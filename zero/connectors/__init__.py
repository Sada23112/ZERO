"""Project ZERO — Service Connectors Subpackage."""

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

__all__ = [
    "BaseConnector",
    "GmailConnector",
    "GoogleCalendarConnector",
    "GoogleDriveConnector",
    "GitHubConnector",
    "OutlookConnector",
    "OneDriveConnector",
    "SlackConnector",
    "DiscordConnector",
    "NotionConnector",
    "SpotifyConnector",
]
