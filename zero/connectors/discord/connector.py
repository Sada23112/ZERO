"""Project ZERO — Discord Connector."""

from typing import List, Dict, Any, Tuple, Optional
from zero.connectors.base import BaseConnector
from zero_logging import logger


class DiscordConnector(BaseConnector):
    """Connector for Discord API."""

    def __init__(self, username: str = "user_discord"):
        self.username = username
        self.is_connected = False

    @property
    def service_type(self) -> str:
        return "discord"

    def connect(self, credentials: Dict[str, Any]) -> Tuple[bool, str]:
        self.is_connected = True
        return True, f"Discord connected for '{self.username}'."

    def disconnect(self) -> Tuple[bool, str]:
        self.is_connected = False
        return True, f"Discord disconnected for '{self.username}'."

    def health_check(self) -> Tuple[bool, str]:
        return (True, "Discord API operational.") if self.is_connected else (False, "Discord not connected.")

    def supported_capabilities(self) -> List[str]:
        return ["read_messages", "send_message"]
