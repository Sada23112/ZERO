"""Project ZERO — Conversation Manager.

Manages active conversation sessions, message persistence, and history truncation.
"""

from typing import List, Optional
from models.conversation import Message, Session, MessageRole
from memory.repository import ConversationRepository
from zero_logging import logger


class ConversationManager:
    """Manages active conversation session lifecycle and persistence."""

    def __init__(self, conv_repo: ConversationRepository):
        self.conv_repo = conv_repo
        self._active_session: Optional[Session] = None

    @property
    def active_session(self) -> Session:
        """Get or create default active session."""
        if not self._active_session:
            self._active_session = self.conv_repo.create_session("Default Session")
        return self._active_session

    def new_session(self, title: str = "New Session") -> Session:
        """Start a new session."""
        self._active_session = self.conv_repo.create_session(title=title)
        logger.info(f"Created new conversation session: {self._active_session.id} ({title})")
        return self._active_session

    def append_message(
        self,
        role: MessageRole,
        content: str,
        session_id: Optional[str] = None,
        model: Optional[str] = None
    ) -> Message:
        """Append and persist a message in the conversation session."""
        target_session_id = session_id or self.active_session.id
        msg = Message(
            session_id=target_session_id,
            role=role,
            content=content,
            model=model
        )
        self.conv_repo.add_message(msg)
        return msg

    def load_history(self, session_id: Optional[str] = None, limit: Optional[int] = 20) -> List[Message]:
        """Load message history for a session."""
        target_session_id = session_id or self.active_session.id
        return self.conv_repo.get_session_messages(target_session_id, limit=limit)

    def summarize_long_conversation(self, session_id: Optional[str] = None) -> str:
        """Placeholder hook for compressing long context histories into a concise summary."""
        target_session_id = session_id or self.active_session.id
        messages = self.load_history(target_session_id)
        if not messages:
            return "Empty conversation session."

        summary = f"Conversation containing {len(messages)} turns."
        logger.debug(f"Summarized session {target_session_id}: {summary}")
        return summary
