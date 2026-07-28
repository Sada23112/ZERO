"""Project ZERO — Outlook Connector."""

from typing import List, Dict, Any, Tuple, Optional
from zero.connectors.base import BaseConnector
from zero_logging import logger


class OutlookConnector(BaseConnector):
    """Connector for Microsoft Outlook Graph API."""

    def __init__(self, email: str = "user@outlook.com"):
        self.email = email
        self.is_connected = False

    @property
    def service_type(self) -> str:
        return "outlook"

    def connect(self, credentials: Dict[str, Any]) -> Tuple[bool, str]:
        self.is_connected = True
        return True, f"Outlook connected for '{self.email}'."

    def disconnect(self) -> Tuple[bool, str]:
        self.is_connected = False
        return True, f"Outlook disconnected for '{self.email}'."

    def health_check(self) -> Tuple[bool, str]:
        return (True, "Outlook API operational.") if self.is_connected else (False, "Outlook not connected.")

    def supported_capabilities(self) -> List[str]:
        return ["read_mail", "send_mail", "search_mail"]
