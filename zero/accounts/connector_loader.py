"""Project ZERO — Service Connector Loader.

Dynamically loads and instantiates service connectors from zero/connectors/.
"""

from typing import Optional, Dict, Any, Type
from zero_logging import logger
from zero.connectors.base import BaseConnector
from zero.connectors.gmail.connector import GmailConnector
from zero.connectors.google_calendar.connector import GoogleCalendarConnector
from zero.connectors.google_drive.connector import GoogleDriveConnector
from zero.connectors.github.connector import GitHubConnector
from zero.connectors.outlook.connector import OutlookConnector
from zero.connectors.onedrive.connector import OneDriveConnector
from zero.connectors.slack.connector import SlackConnector
from zero.connectors.discord.connector import DiscordConnector
from zero.connectors.notion.connector import NotionConnector
from zero.connectors.spotify.connector import SpotifyConnector

CONNECTOR_REGISTRY: Dict[str, Type[BaseConnector]] = {
    "google": GmailConnector,
    "gmail": GmailConnector,
    "google_calendar": GoogleCalendarConnector,
    "google_drive": GoogleDriveConnector,
    "github": GitHubConnector,
    "outlook": OutlookConnector,
    "onedrive": OneDriveConnector,
    "slack": SlackConnector,
    "discord": DiscordConnector,
    "notion": NotionConnector,
    "spotify": SpotifyConnector,
}


class ConnectorLoader:
    """Dynamic factory and loader for external service connectors."""

    @staticmethod
    def get_connector(service_type: str, **kwargs: Any) -> Optional[BaseConnector]:
        """Instantiate target service connector."""
        st = service_type.lower().strip()
        cls = CONNECTOR_REGISTRY.get(st)
        if cls:
            try:
                return cls(**kwargs)
            except Exception as e:
                logger.error(f"[ConnectorLoader] Failed to instantiate '{st}' connector: {e}")
                return cls()
        logger.warning(f"[ConnectorLoader] Unknown service connector: '{service_type}'")
        return None
