"""Project ZERO — Task Manager Subsystem (Phase 4 Capability #16)."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TaskItem(BaseModel):
    """Task item data model."""

    id: str
    title: str
    priority: str = "medium"  # 'high', 'medium', 'low'
    status: str = "todo"      # 'todo', 'in_progress', 'completed'
    dependencies: List[str] = Field(default_factory=list)
    notes: str = ""


class TaskManager:
    """Manages project tasks, priorities, dependencies, & progress tracking."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "task_manager.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: List[TaskItem] = self._load()

    def _load(self) -> List[TaskItem]:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [TaskItem(**item) for item in data]
            except Exception:
                pass
        return []

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([t.model_dump() for t in self.tasks], f, indent=2)
        except Exception:
            pass

    def create_task(self, title: str, priority: str = "medium", notes: str = "") -> TaskItem:
        """Create a new task."""
        task = TaskItem(
            id=f"task_{len(self.tasks) + 1}",
            title=title,
            priority=priority,
            notes=notes
        )
        self.tasks.append(task)
        self._save()
        return task

    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed."""
        for t in self.tasks:
            if t.id == task_id:
                t.status = "completed"
                self._save()
                return True
        return False

    def list_tasks(self, status: Optional[str] = None) -> List[TaskItem]:
        """List tasks with optional status filter."""
        if status:
            return [t for t in self.tasks if t.status == status]
        return self.tasks
