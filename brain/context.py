"""Project ZERO — Context Engine.

Assembles dynamic context prompts from session history, relevant memory records,
and workspace information without hardcoding static prompts.
"""

from pathlib import Path
from typing import List, Optional
from models.conversation import Message
from models.memory import MemoryRecord
from memory.repository import MemoryRepository, ConversationRepository


class ContextBuilder:
    """Dynamically gathers and builds context prompts for the central Brain coordinator."""

    def __init__(
        self,
        memory_repo: MemoryRepository,
        conv_repo: ConversationRepository,
        workspace_root: Optional[Path] = None
    ):
        self.memory_repo = memory_repo
        self.conv_repo = conv_repo
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def build_system_instruction(self, user_query: str) -> str:
        """Construct system instruction prompt including ZERO's identity and active memories."""
        base_instruction = (
            "You are Project ZERO, a personal autonomous intelligence platform and lifelong engineering companion.\n"
            "Your mission is to increase the user's ability to think, learn, design, invent, and create.\n"
            "Be direct, honest, highly capable, and precise. Never fake data or hallucinate tool outputs.\n"
            "Format code blocks and responses in clean GitHub markdown.\n"
        )

        # Gather relevant memories matching user query keywords
        relevant_memories: List[MemoryRecord] = []
        if user_query and user_query.strip():
            # Extract keywords from user query
            words = [w.strip() for w in user_query.split() if len(w.strip()) > 3]
            for w in words:
                matches = self.memory_repo.search(w, limit=5)
                for m in matches:
                    if not any(existing.id == m.id for existing in relevant_memories):
                        relevant_memories.append(m)

        memory_section = ""
        if relevant_memories:
            memory_lines = [f"- {mem.key}: {mem.value}" for mem in relevant_memories]
            memory_section = (
                "\n[Relevant Cognitive Memory Context]\n" +
                "\n".join(memory_lines) + "\n"
            )

        workspace_info = f"\n[Active Workspace Root]\n{self.workspace_root}\n"

        return f"{base_instruction}{memory_section}{workspace_info}"

    def gather_conversation_history(self, session_id: str, limit: int = 15) -> List[Message]:
        """Fetch recent message history for current active session."""
        return self.conv_repo.get_session_messages(session_id, limit=limit)
