"""Project ZERO — Central Brain Coordinator.

The Brain is the central coordinator of Project ZERO.
No CLI or client directly invokes providers or tools. All input flows through Brain.
"""

import asyncio
from typing import AsyncGenerator, Optional, Dict, Any, List
from config import get_settings, ZeroSettings
from memory.database import DatabaseManager
from memory.repository import MemoryRepository, ConversationRepository
from memory.repository import MemoryCategory
from brain.context import ContextBuilder
from brain.conversation import ConversationManager
from providers.gemini import GeminiProvider
from providers.registry import ProviderRegistry, provider_registry
from tools.registry import ToolRegistry, tool_registry
from models.conversation import Message, MessageRole
from zero_logging import logger


class Brain:
    """Central Coordinator for reasoning, memory retrieval, tool execution, and provider invocation."""

    def __init__(
        self,
        settings: Optional[ZeroSettings] = None,
        db_manager: Optional[DatabaseManager] = None
    ):
        self.settings = settings or get_settings()
        self.db_manager = db_manager or DatabaseManager(self.settings.database_path)

        self.conv_repo = ConversationRepository(self.db_manager)
        self.memory_repo = MemoryRepository(self.db_manager)

        self.context_builder = ContextBuilder(self.memory_repo, self.conv_repo)
        self.conversation_manager = ConversationManager(self.conv_repo)

        # Provider initialization
        self.provider = GeminiProvider(self.settings.gemini_api_key)
        provider_registry.register_provider(self.provider)

        # Tool registry reference
        self.tool_registry = tool_registry

    async def process(self, prompt: str) -> str:
        """Process user input through memory retrieval, context building, tool execution, and LLM reasoning."""
        clean_prompt = prompt.strip()
        if not clean_prompt:
            return ""

        # 1. Handle Explicit Natural Language Memory Triggers
        memory_result = await self._check_memory_triggers(clean_prompt)
        if memory_result is not None:
            return memory_result

        # 2. Handle Explicit Tool Execution Triggers
        tool_result = await self._check_tool_triggers(clean_prompt)
        if tool_result is not None:
            return tool_result

        # 3. Standard Cognitive Flow: Context Assembly & Provider Generation
        # Record user message in session
        self.conversation_manager.append_message(
            role=MessageRole.USER,
            content=clean_prompt
        )

        # Build dynamic context and system instruction
        system_instruction = self.context_builder.build_system_instruction(clean_prompt)
        history = self.conversation_manager.load_history(limit=10)

        # Invoke provider
        response_text = await self.provider.generate_response(
            messages=history,
            model=self.settings.default_model,
            system_instruction=system_instruction
        )

        # Persist assistant response
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

        # Check memory triggers first
        memory_res = await self._check_memory_triggers(clean_prompt)
        if memory_res is not None:
            yield memory_res
            return

        # Check tool triggers
        tool_res = await self._check_tool_triggers(clean_prompt)
        if tool_res is not None:
            yield tool_res
            return

        # Record user message
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

        # Persist complete response
        complete_text = "".join(full_response)
        self.conversation_manager.append_message(
            role=MessageRole.ASSISTANT,
            content=complete_text,
            model=self.settings.default_model
        )

    async def _check_memory_triggers(self, prompt: str) -> Optional[str]:
        """Intercept and handle memory commands (e.g. 'remember that X uses Y', 'list my memories', 'search memory X')."""
        lower = prompt.lower()

        # "remember that X uses/is Y" or "remember X"
        if lower.startswith("remember that ") or lower.startswith("remember "):
            content_to_remember = prompt[9:].strip() if lower.startswith("remember ") else prompt[14:].strip()
            if " uses " in content_to_remember:
                key, val = content_to_remember.split(" uses ", 1)
                record = self.memory_repo.store(key=key.strip(), value=f"uses {val.strip()}", category=MemoryCategory.PROJECT_FACT)
            elif " is " in content_to_remember:
                key, val = content_to_remember.split(" is ", 1)
                record = self.memory_repo.store(key=key.strip(), value=val.strip(), category=MemoryCategory.PROJECT_FACT)
            else:
                record = self.memory_repo.store(key=f"fact_{len(self.memory_repo.list()) + 1}", value=content_to_remember, category=MemoryCategory.GENERAL)
            
            return f"Recorded memory: {record.key} -> {record.value}"

        # "what framework does X use?" or "what does X use?"
        if lower.startswith("what framework does ") or lower.startswith("what does "):
            subject = lower.replace("what framework does ", "").replace("what does ", "").replace(" use?", "").replace(" use", "").strip()
            matches = self.memory_repo.search(subject)
            if matches:
                return f"{matches[0].key.title()} uses {matches[0].value.replace('uses ', '')}."
            return f"No memory record found for '{subject}'."

        # "list my memories" or "list memories"
        if lower in ["list my memories", "list memories"]:
            mems = self.memory_repo.list()
            if not mems:
                return "No saved memories found."
            lines = [f"- {m.key}: {m.value} [{m.category.value}]" for m in mems]
            return "Saved Memories:\n" + "\n".join(lines)

        # "search memory X"
        if lower.startswith("search memory "):
            q = prompt[14:].strip()
            mems = self.memory_repo.search(q)
            if not mems:
                return f"No memories found matching '{q}'."
            lines = [f"- {m.key}: {m.value}" for m in mems]
            return f"Memory search results for '{q}':\n" + "\n".join(lines)

        return None

    async def _check_tool_triggers(self, prompt: str) -> Optional[str]:
        """Intercept and route explicit tool requests (read file, run command, open url, summarize folder)."""
        lower = prompt.lower()

        # "read <file>"
        if lower.startswith("read ") and not lower.startswith("read this "):
            filename = prompt[5:].strip()
            res = await self.tool_registry.execute_tool("c1", "read_file", {"path": filename})
            return res.output if res.success else f"Error reading file: {res.error}"

        # "summarize <folder>" or "summarize this folder"
        if lower.startswith("summarize "):
            folder = prompt[10:].strip()
            if folder in ["this folder", "src/", "."]:
                folder = "."
            res = await self.tool_registry.execute_tool("c2", "list_directory", {"path": folder})
            if res.success:
                return f"Summary of folder '{folder}':\n{res.output}"
            return f"Error listing directory: {res.error}"

        # "run <command>"
        if lower.startswith("run ") or lower.startswith("execute "):
            cmd = prompt.split(" ", 1)[1].strip()
            res = await self.tool_registry.execute_tool("c3", "run_command", {"command": cmd})
            return f"[Command Output (exit {0 if res.success else 1})]:\n{res.output}"

        # "open <target>" (e.g. "open youtube", "open python.org", "open https://google.com")
        if lower.startswith("open "):
            target = prompt[5:].strip()
            if target:
                res = await self.tool_registry.execute_tool("c4", "open_url", {"url": target})
                return res.output if res.success else f"Error opening URL: {res.error}"

        return None
