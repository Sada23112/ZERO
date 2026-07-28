"""Project ZERO — Long-Running Planning Engine (Phase 4 Capability #24)."""

import asyncio
from typing import List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field
from zero_logging import logger


class PlanStep(BaseModel):
    """Single step in execution plan."""

    step_id: int
    description: str
    status: str = "pending"  # 'pending', 'in_progress', 'completed', 'failed'
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None


class ExecutionPlan(BaseModel):
    """Multi-step execution plan."""

    plan_id: str
    goal: str
    steps: List[PlanStep] = Field(default_factory=list)
    is_completed: bool = False


class LongRunningPlanningEngine:
    """Orchestrates long-running multi-step plan execution, retries, and goal tracking."""

    def __init__(self):
        self.active_plans: Dict[str, ExecutionPlan] = {}

    def create_plan(self, plan_id: str, goal: str, step_descriptions: List[str]) -> ExecutionPlan:
        """Create execution plan with sequential steps."""
        steps = [
            PlanStep(step_id=i + 1, description=desc)
            for i, desc in enumerate(step_descriptions)
        ]
        plan = ExecutionPlan(plan_id=plan_id, goal=goal, steps=steps)
        self.active_plans[plan_id] = plan
        logger.info(f"Created execution plan '{plan_id}' with {len(steps)} steps.")
        return plan

    async def execute_plan(self, plan_id: str, step_executor: Callable[[PlanStep], Any]) -> bool:
        """Execute plan steps sequentially with failure retry logic."""
        plan = self.active_plans.get(plan_id)
        if not plan:
            logger.error(f"Plan '{plan_id}' not found.")
            return False

        for step in plan.steps:
            if step.status == "completed":
                continue

            step.status = "in_progress"
            success = False

            while step.retry_count < step.max_retries and not success:
                try:
                    await step_executor(step)
                    step.status = "completed"
                    success = True
                except Exception as err:
                    step.retry_count += 1
                    step.error_message = str(err)
                    logger.warning(f"Step {step.step_id} failed (attempt {step.retry_count}/{step.max_retries}): {err}")
                    await asyncio.sleep(0.5)

            if not success:
                step.status = "failed"
                logger.error(f"Plan '{plan_id}' failed at step {step.step_id}.")
                return False

        plan.is_completed = True
        logger.info(f"Plan '{plan_id}' completed successfully.")
        return True
