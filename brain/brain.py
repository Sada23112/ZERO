"""Project ZERO — Central Brain Coordinator (Phase 7 Operating System Intelligence).

The Brain is the central coordinator of Project ZERO.
All inputs flow through Brain, which coordinates reasoning, memory retrieval, context awareness, OS intelligence, tool execution, and self-evolution.
"""

import os
import asyncio
from pathlib import Path
from typing import AsyncGenerator, Optional, Dict, Any, List
from config import get_settings, ZeroSettings
from memory.database import DatabaseManager
from memory.repository import MemoryRepository, ConversationRepository
from memory.repository import MemoryCategory
from memory.knowledge_graph import CognitiveKnowledgeGraph
from memory.project_knowledge import ProjectKnowledgeStore
from brain.context import ContextBuilder
from brain.conversation import ConversationManager
from brain.prompts import PromptLibrary
from brain.session_replay import SessionReplayer
from intelligence.codebase import CodebaseIntelligence
from intelligence.search import SemanticSearchEngine
from intelligence.research import InternetResearchEngine
from intelligence.notebook import ResearchNotebook
from planner.task_manager import TaskManager
from planner.engine import LongRunningPlanningEngine
from security.failsafe import FailsafeSystem
from evolution.engine import EvolutionEngine
from evolution.capability_detector import CapabilityDetector
from evolution.rollback import RollbackEngine
from evolution.repair_engine import SelfRepairEngine
from awareness.context_manager import ContextManager, SystemContext
from operating_system.system_context import OSSystemContext
from operating_system.desktop_environment import DesktopEnvironment
from providers.gemini import GeminiProvider
from providers.registry import ProviderRegistry, provider_registry
from tools.registry import ToolRegistry, tool_registry
from models.conversation import Message, MessageRole
from zero_logging import logger


class Brain:
    """Central Coordinator for reasoning, OS awareness, memory retrieval, tool execution, provider invocation, & self-evolution."""

    def __init__(
        self,
        settings: Optional[ZeroSettings] = None,
        db_manager: Optional[DatabaseManager] = None
    ):
        self.settings = settings or get_settings()
        self.db_manager = db_manager or DatabaseManager(self.settings.database_path)

        self.conv_repo = ConversationRepository(self.db_manager)
        self.memory_repo = MemoryRepository(self.db_manager)

        # Phase 6 Awareness Subsystem
        self.context_manager = ContextManager()

        # Phase 7 OS Intelligence Subsystem
        self.os_context = OSSystemContext()

        self.context_builder = ContextBuilder(self.memory_repo, self.conv_repo, self.context_manager)
        self.conversation_manager = ConversationManager(self.conv_repo)

        # Phase 4 Subsystems
        self.failsafe = FailsafeSystem()
        self.knowledge_graph = CognitiveKnowledgeGraph()
        self.project_knowledge = ProjectKnowledgeStore()
        self.codebase_intel = CodebaseIntelligence()
        self.search_engine = SemanticSearchEngine()
        self.research_engine = InternetResearchEngine()
        self.research_notebook = ResearchNotebook()
        self.task_manager = TaskManager()
        self.planning_engine = LongRunningPlanningEngine()
        self.prompt_library = PromptLibrary()
        self.session_replayer = SessionReplayer(self.conv_repo)

        # Phase 5 Evolution Subsystems
        self.evolution_engine = EvolutionEngine()
        self.capability_detector = CapabilityDetector(self.evolution_engine.registry_store)
        self.rollback_engine = RollbackEngine(registry_store=self.evolution_engine.registry_store)
        self.repair_engine = SelfRepairEngine()

        # Provider initialization
        self.provider = GeminiProvider(self.settings.gemini_api_key)
        provider_registry.register_provider(self.provider)

        # Tool registry reference
        self.tool_registry = tool_registry

    async def process(self, prompt: str) -> str:
        """Process user input through OS intelligence, awareness, tool execution, self-evolution, and LLM reasoning."""
        clean_prompt = prompt.strip()
        if not clean_prompt:
            return ""

        self.context_manager.session_context.record_activity(clean_prompt)
        self.context_manager.activity_logger.log_event("command", clean_prompt)

        # 1. Handle Phase 7 Operating System Intelligence Commands
        os_intel_res = await self._check_os_intelligence_triggers(clean_prompt)
        if os_intel_res is not None:
            return os_intel_res

        # 2. Handle Phase 6 Awareness & Natural References Triggers
        awareness_res = await self._check_awareness_triggers(clean_prompt)
        if awareness_res is not None:
            return awareness_res

        # 3. Handle Explicit Natural Language Memory Triggers
        memory_result = await self._check_memory_triggers(clean_prompt)
        if memory_result is not None:
            return memory_result

        # 4. Handle Phase 5 Self-Evolution & Self-Repair Commands
        evolution_cmd_res = await self._check_evolution_commands(clean_prompt)
        if evolution_cmd_res is not None:
            return evolution_cmd_res

        # 5. Handle Explicit Tool Triggers & Missing Capability Detection
        tool_result = await self._check_tool_triggers(clean_prompt)
        if tool_result is not None:
            return tool_result

        # 6. Standard Cognitive Flow: Context Assembly & Provider Generation
        self.conversation_manager.append_message(
            role=MessageRole.USER,
            content=clean_prompt
        )

        system_instruction = self.context_builder.build_system_instruction(clean_prompt)
        history = self.conversation_manager.load_history(limit=10)

        response_text = await self.provider.generate_response(
            messages=history,
            model=self.settings.default_model,
            system_instruction=system_instruction
        )

        self.conversation_manager.append_message(
            role=MessageRole.ASSISTANT,
            content=response_text,
            model=self.settings.default_model
        )

        return response_text

    async def process_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response chunks from Brain."""
        clean_prompt = prompt.strip()
        if not clean_prompt:
            yield ""
            return

        self.context_manager.session_context.record_activity(clean_prompt)

        os_res = await self._check_os_intelligence_triggers(clean_prompt)
        if os_res is not None:
            yield os_res
            return

        awareness_res = await self._check_awareness_triggers(clean_prompt)
        if awareness_res is not None:
            yield awareness_res
            return

        memory_res = await self._check_memory_triggers(clean_prompt)
        if memory_res is not None:
            yield memory_res
            return

        evo_cmd_res = await self._check_evolution_commands(clean_prompt)
        if evo_cmd_res is not None:
            yield evo_cmd_res
            return

        tool_res = await self._check_tool_triggers(clean_prompt)
        if tool_res is not None:
            yield tool_res
            return

        self.conversation_manager.append_message(
            role=MessageRole.USER,
            content=clean_prompt
        )

        system_instruction = self.context_builder.build_system_instruction(clean_prompt)
        history = self.conversation_manager.load_history(limit=10)

        full_response = []
        async for chunk in self.provider.stream_generate(
            messages=history,
            model=self.settings.default_model,
            system_instruction=system_instruction
        ):
            full_response.append(chunk)
            yield chunk

        complete_text = "".join(full_response)
        self.conversation_manager.append_message(
            role=MessageRole.ASSISTANT,
            content=complete_text,
            model=self.settings.default_model
        )

    async def _check_os_intelligence_triggers(self, prompt: str) -> Optional[str]:
        """Intercept and resolve Phase 7 Operating System Intelligence commands."""
        lower = prompt.lower().strip()

        # Application Launching
        if lower.startswith("open ") or lower.startswith("launch "):
            app_target = lower.replace("open ", "").replace("launch ", "").strip()

            # 1. Check Standard OS Folders
            std_dir = self.os_context.path_resolver.get_standard_directory(app_target)
            if std_dir:
                DesktopEnvironment.open_path(std_dir)
                return f"Opened OS directory: {std_dir}"

            # 2. Check Applications
            launched = self.os_context.app_manager.launch_application(app_target)
            if launched:
                return f"Launched application: '{app_target}'"

            # 3. Check Newest File Search
            if "newest pdf" in lower or "latest pdf" in lower:
                target_file = self.os_context.path_resolver.resolve_newest_file(category="documents")
                if target_file:
                    DesktopEnvironment.open_path(target_file)
                    return f"Opened newest PDF document: {target_file}"

            if "download" in lower:
                recent_dls = self.os_context.recent_tracker.get_recent_downloads(limit=1)
                if recent_dls:
                    DesktopEnvironment.open_path(recent_dls[0])
                    return f"Opened recent download: {recent_dls[0]}"

        # OS Storage Analytics
        if lower in ["show me my largest folders", "show largest folders", "show largest files", "disk space", "storage info"]:
            rep = self.os_context.storage_manager.get_storage_report()
            files_str = "\n".join([f"- {f['name']} ({f['size_mb']} MB): {f['path']}" for f in rep.largest_files[:5]])
            return (
                f"Storage Intelligence Analytics:\n"
                f"- Disk Usage: {rep.used_gb} GB used / {rep.total_gb} GB total ({rep.percent_used}%)\n"
                f"- Free Space: {rep.free_gb} GB\n"
                f"Largest Files:\n{files_str or '- None over 10MB found.'}"
            )

        # OS-Wide Project Auto-Discovery
        if lower.startswith("where is my ") or lower.startswith("find my ") or lower in ["discover projects"]:
            q = lower.replace("where is my ", "").replace("find my ", "").replace(" project", "").replace(" projects", "").strip()
            projs = self.os_context.workspace_manager.discover_projects(max_depth=3)
            matches = [p for p in projs if q in p.name.lower() or q in p.project_type.lower()]
            if matches:
                lines = [f"- {p.name} [{p.project_type}]: {p.path}" for p in matches]
                return f"Discovered Projects matching '{q}':\n" + "\n".join(lines)
            elif projs:
                lines = [f"- {p.name} [{p.project_type}]: {p.path}" for p in projs[:5]]
                return "Discovered OS Projects:\n" + "\n".join(lines)

        return None

    async def _check_awareness_triggers(self, prompt: str) -> Optional[str]:
        """Intercept and resolve Phase 6 Context & Awareness natural language queries."""
        lower = prompt.lower().strip()

        if lower in ["good morning", "good afternoon", "good evening", "hello", "hi"]:
            greeting = self.context_manager.calendar_awareness.get_greeting()
            cal = self.context_manager.calendar_awareness.get_current_info()
            return f"{greeting}. Today is {cal['weekday']}, {cal['month']} {cal['year']} ({cal['current_time']}). Active project: {self.context_manager.workspace_awareness.workspace_root.name}."

        if lower in [
            "what did we work on yesterday?",
            "what were we doing before lunch?",
            "continue yesterday's work",
            "continue my last project",
            "resume the interrupted task"
        ]:
            return self.context_manager.daily_memory.get_yesterdays_summary()

        if lower in ["summarize today's work", "what happened this morning?", "what happened this afternoon?"]:
            return self.context_manager.daily_memory.get_todays_summary()

        if lower in ["what have you learned recently?", "what have you learned from recent repairs?"]:
            ref = self.context_manager.experience_engine.get_reflections()
            return f"Recent Learning Insights:\n{ref['recent_lessons']}"

        if lower in ["which generated tools are most reliable?", "which tools are most reliable?"]:
            ref = self.context_manager.experience_engine.get_reflections()
            rel = ", ".join(ref['reliable_tools'])
            return f"Most Reliable Subsystems & Tools:\n- {rel}"

        if lower in ["what capabilities fail most often?", "what should you improve?"]:
            ref = self.context_manager.experience_engine.get_reflections()
            return f"System Failures & Bottlenecks:\n- {ref['frequent_failures']}"

        if lower in ["what projects do you know best?", "active project"]:
            ws = self.context_manager.workspace_awareness.get_workspace_info()
            return f"Known Projects:\n- Active Workspace: {ws['project_name']} ({ws['workspace_root']})\n- Active Branch: {ws['git_branch']}"

        return None

    async def _check_evolution_commands(self, prompt: str) -> Optional[str]:
        """Intercept and handle Phase 5 Evolution, Rollback, & Self-Repair commands."""
        lower = prompt.lower().strip()

        if lower == "rollback last evolution":
            success = self.rollback_engine.rollback_last_evolution()
            return "Successfully rolled back last capability evolution." if success else "No active evolutions to rollback."

        if lower.startswith("rollback capability "):
            cap_name = lower.replace("rollback capability ", "").replace("rollback ", "").strip()
            success = self.rollback_engine.rollback_capability(cap_name)
            return f"Successfully rolled back capability '{cap_name}'." if success else f"Capability '{cap_name}' not found."

        if lower in ["show evolution history", "evolution history"]:
            recs = self.evolution_engine.history_store.records
            if not recs:
                return "Evolution history is empty."
            lines = [f"- [{r.record_id}] {r.action_type.upper()} {r.capability_name}: {r.status} ({r.user_prompt})" for r in recs]
            return "Evolution History Log:\n" + "\n".join(lines)

        if lower in ["show generated capabilities", "list dynamic capabilities"]:
            caps = self.evolution_engine.registry_store.list_capabilities()
            if not caps:
                return "No dynamically generated capabilities currently active."
            lines = [f"- {c.name} v{c.version}: {c.description}" for c in caps]
            return "Dynamically Generated Active Capabilities:\n" + "\n".join(lines)

        if lower.startswith("repair ") or lower in ["repair yourself", "fix yourself"]:
            target = lower.replace("repair ", "").strip()
            report = self.repair_engine.repair_subsystem(target)
            return f"Self-Repair Report for {report.target_subsystem}:\n- Issue: {report.issue_detected}\n- Status: {report.message}"

        return None

    async def _check_memory_triggers(self, prompt: str) -> Optional[str]:
        """Intercept and handle memory commands & knowledge graph queries."""
        lower = prompt.lower()

        if lower.startswith("remember that ") or lower.startswith("remember "):
            content_to_remember = prompt[9:].strip() if lower.startswith("remember ") else prompt[14:].strip()
            if " uses " in content_to_remember:
                key, val = content_to_remember.split(" uses ", 1)
                record = self.memory_repo.store(key=key.strip(), value=f"uses {val.strip()}", category=MemoryCategory.PROJECT_FACT)
                self.knowledge_graph.add_relation(key.strip(), "uses", val.strip())
            elif " is " in content_to_remember:
                key, val = content_to_remember.split(" is ", 1)
                record = self.memory_repo.store(key=key.strip(), value=val.strip(), category=MemoryCategory.PROJECT_FACT)
                self.knowledge_graph.add_relation(key.strip(), "is", val.strip())
            else:
                record = self.memory_repo.store(key=f"fact_{len(self.memory_repo.list()) + 1}", value=content_to_remember, category=MemoryCategory.GENERAL)
            
            return f"Recorded memory & graph link: {record.key} -> {record.value}"

        if lower.startswith("what framework does ") or lower.startswith("what does "):
            subject = lower.replace("what framework does ", "").replace("what does ", "").replace(" use?", "").replace(" use", "").strip()
            matches = self.memory_repo.search(subject)
            if matches:
                return f"{matches[0].key.title()} uses {matches[0].value.replace('uses ', '')}."
            return f"No memory record found for '{subject}'."

        if lower in ["list my memories", "list memories"]:
            mems = self.memory_repo.list()
            if not mems:
                return "No saved memories found."
            lines = [f"- {m.key}: {m.value} [{m.category.value}]" for m in mems]
            return "Saved Memories:\n" + "\n".join(lines)

        if lower.startswith("search memory "):
            q = prompt[14:].strip()
            mems = self.memory_repo.search(q)
            if not mems:
                return f"No memories found matching '{q}'."
            lines = [f"- {m.key}: {m.value}" for m in mems]
            return f"Memory search results for '{q}':\n" + "\n".join(lines)

        if lower.startswith("graph ") or lower.startswith("knowledge graph "):
            q = prompt.split(" ", 2)[-1].strip()
            res = self.knowledge_graph.query_entity(q)
            if res["relationships"]:
                return f"Knowledge Graph Network for '{q}':\n" + "\n".join(res["relationships"])
            return f"No knowledge graph relationships found for '{q}'."

        return None

    async def _check_tool_triggers(self, prompt: str) -> Optional[str]:
        """Intercept and route explicit tool & capability requests or trigger self-evolution."""
        lower = prompt.lower()

        det_res = self.capability_detector.detect_capability(prompt)
        if det_res.action_type == "generate_new" and det_res.tool_name:
            evo_res = await self.evolution_engine.evolve_capability(det_res.tool_name, prompt)
            if evo_res.success:
                return f"[{evo_res.message}]\n{evo_res.output}"
            else:
                return f"Evolution failed: {evo_res.message}"

        if lower.startswith("git ") or lower == "git":
            sub = lower[4:].strip() if len(lower) > 4 else "status"
            res = await self.tool_registry.execute_tool("git_call", "git_tool", {"subcommand": sub})
            return res.output if res.success else f"Git error: {res.error}"

        if lower in ["analyze project", "analyze codebase"]:
            analysis = self.codebase_intel.analyze_project()
            return (
                f"Codebase Intelligence Report:\n"
                f"- Total Files: {analysis.total_files}\n"
                f"- Languages: {', '.join(analysis.languages)}\n"
                f"- Frameworks/Managers: {', '.join(analysis.package_managers)}\n"
                f"- Entry Points: {', '.join(analysis.entry_points)}\n"
                f"- Config Files: {', '.join(analysis.config_files)}"
            )

        if lower.startswith("search code ") or lower.startswith("search todo"):
            if lower == "search todo" or lower == "search todos":
                matches = self.search_engine.search_todos()
            else:
                q = prompt[12:].strip()
                matches = self.search_engine.search_pattern(q)
            if not matches:
                return "No search results found."
            lines = [f"{m.file_path}:{m.line_number} -> {m.line_content}" for m in matches[:15]]
            return "Search Results:\n" + "\n".join(lines)

        if lower.startswith("read document ") or lower.startswith("parse doc "):
            path = prompt.split(" ", 2)[-1].strip()
            res = await self.tool_registry.execute_tool("doc_call", "document_reader", {"path": path})
            return res.output if res.success else f"Document error: {res.error}"

        if lower in ["capture screen", "screenshot", "take screenshot"]:
            res = await self.tool_registry.execute_tool("vis_call", "vision_capture", {})
            return res.output if res.success else f"Vision error: {res.error}"

        if lower in ["metrics", "system metrics", "cpu usage", "ram usage"]:
            res = await self.tool_registry.execute_tool("proc_call", "process_manager", {"action": "metrics"})
            return res.output if res.success else f"Metrics error: {res.error}"

        if lower in ["process list", "list processes"]:
            res = await self.tool_registry.execute_tool("proc_call", "process_manager", {"action": "list"})
            return res.output if res.success else f"Process list error: {res.error}"

        if lower in ["health check", "diagnostics", "system health"]:
            from cli.diagnostics import SelfDiagnostics
            report = SelfDiagnostics().run_health_check()
            return (
                f"System Health & Diagnostics Report:\n"
                f"- Database Healthy: {report.database_healthy}\n"
                f"- Provider Healthy: {report.provider_healthy}\n"
                f"- Registered Tools: {report.registered_tools_count}\n"
                f"- Workspace Writable: {report.workspace_writable}\n"
                f"- Issues Found: {len(report.issues_found)}"
            )

        if lower.startswith("read ") and not lower.startswith("read this "):
            filename = prompt[5:].strip()
            res = await self.tool_registry.execute_tool("c1", "read_file", {"path": filename})
            return res.output if res.success else f"Error reading file: {res.error}"

        if lower.startswith("summarize "):
            folder = prompt[10:].strip()
            if folder in ["this folder", "src/", "."]:
                folder = "."
            res = await self.tool_registry.execute_tool("c2", "list_directory", {"path": folder})
            if res.success:
                return f"Summary of folder '{folder}':\n{res.output}"
            return f"Error listing directory: {res.error}"

        if lower.startswith("run ") or lower.startswith("execute "):
            cmd = prompt.split(" ", 1)[1].strip()
            res = await self.tool_registry.execute_tool("c3", "run_command", {"command": cmd})
            return f"[Command Output (exit {0 if res.success else 1})]:\n{res.output}"

        if lower.startswith("open "):
            target = prompt[5:].strip()
            if target:
                res = await self.tool_registry.execute_tool("c4", "open_url", {"url": target})
                return res.output if res.success else f"Error opening URL: {res.error}"

        return None
