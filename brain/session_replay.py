"""Project ZERO — Session Replay & Yesterday Summarizer (Phase 4 Capability #19)."""

from typing import List, Optional
from memory.repository import ConversationRepository
from models.conversation import Message
from zero_logging import logger


class SessionReplayer:
    """Replays previous sessions and summarizes past activity (e.g. 'summarize yesterday')."""

    def __init__(self, conv_repo: ConversationRepository):
        self.conv_repo = conv_repo

    def summarize_yesterday(self, session_id: Optional[str] = None) -> str:
        """Summarize conversation activity from previous sessions."""
        messages: List[Message] = self.conv_repo.get_session_messages(session_id or "default", limit=50)
        if not messages:
            return "No previous session activity recorded."

        user_prompts = [m.content for m in messages if m.role.value == "user"]
        summary = f"Yesterday's Session Activity ({len(user_prompts)} turns):\n"
        for i, p in enumerate(user_prompts[-5:], 1):
            summary += f"{i}. {p}\n"

        return summary
