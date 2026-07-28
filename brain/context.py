"""Project ZERO — Cognitive Context Builder (Phase 6 Context Integration)."""

from pathlib import Path
from typing import List, Optional
from memory.repository import MemoryRepository, ConversationRepository
from awareness.context_manager import ContextManager, SystemContext


class ContextBuilder:
    """Assembles prompt system instructions combining long-term memory & live SystemContext."""

    def __init__(
        self,
        memory_repo: MemoryRepository,
        conversation_repo: ConversationRepository,
        context_manager: Optional[ContextManager] = None,
        workspace_root: Optional[Path] = None
    ):
        self.memory_repo = memory_repo
        self.conversation_repo = conversation_repo
        self.workspace_root = workspace_root
        self.context_manager = context_manager or ContextManager(workspace_root=workspace_root)

    def build_system_instruction(self, current_user_prompt: str) -> str:
        """Construct full system instruction with system awareness context & relevant memories."""
        sys_context: SystemContext = self.context_manager.assemble_context()
        context_str = sys_context.to_system_prompt_str()

        # Search relevant memory records by full prompt or individual words
        relevant_memories = self.memory_repo.search(current_user_prompt)
        if not relevant_memories:
            words = [w.strip() for w in current_user_prompt.split() if len(w.strip()) > 3]
            for w in words:
                mems = self.memory_repo.search(w)
                for m in mems:
                    if not any(rm.id == m.id for rm in relevant_memories):
                        relevant_memories.append(m)

        mem_block = ""
        if relevant_memories:
            mem_lines = [f"- {m.key}: {m.value}" for m in relevant_memories[:5]]
            mem_block = f"\nRelevant Memory Facts:\n" + "\n".join(mem_lines) + "\n"

        base_instruction = (
            "You are Project ZERO, a personal AI engineering operating companion. "
            "Remain terminal-first, local-first, python-first, and highly context-aware. "
            "Be precise, concise, and helpful."
        )

        return f"{base_instruction}\n\n{context_str}\n{mem_block}"
