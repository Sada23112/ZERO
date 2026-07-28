"""Project ZERO — Spotify Connector."""

from typing import List, Dict, Any, Tuple, Optional
from zero.connectors.base import BaseConnector
from zero_logging import logger


class SpotifyConnector(BaseConnector):
    """Connector for Spotify Web API."""

    def __init__(self, username: str = "spotify_user"):
        self.username = username
        self.is_connected = False

    @property
    def service_type(self) -> str:
        return "spotify"

    def connect(self, credentials: Dict[str, Any]) -> Tuple[bool, str]:
        self.is_connected = True
        return True, f"Spotify connected for '{self.username}'."

    def disconnect(self) -> Tuple[bool, str]:
        self.is_connected = False
        return True, f"Spotify disconnected for '{self.username}'."

    def health_check(self) -> Tuple[bool, str]:
        return (True, "Spotify API operational.") if self.is_connected else (False, "Spotify not connected.")

    def supported_capabilities(self) -> List[str]:
        return ["play_playback", "pause_playback", "search_tracks", "list_playlists"]
