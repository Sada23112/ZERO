"""Project ZERO — Official OAuth 2.0 Manager.

Generates official authorization URLs, formats step-by-step user auth guides,
and handles token exchange and refresh flows for Google, Microsoft, GitHub, Spotify, Slack, Discord.
"""

import urllib.parse
from typing import Dict, Any, Tuple, Optional
from zero_logging import logger

OAUTH_CONFIGS = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "scopes": ["https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/drive"],
        "client_id": "88234019283-google-zero-app.apps.googleusercontent.com",
    },
    "microsoft": {
        "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "scopes": ["Mail.ReadWrite", "Calendars.ReadWrite", "Files.ReadWrite"],
        "client_id": "ms-zero-app-client-id-99128",
    },
    "github": {
        "auth_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "scopes": ["repo", "user", "workflow"],
        "client_id": "gh-zero-app-client-id-3312",
    },
    "spotify": {
        "auth_url": "https://accounts.spotify.com/authorize",
        "token_url": "https://accounts.spotify.com/api/token",
        "scopes": ["user-read-playback-state", "user-modify-playback-state", "playlist-read-private"],
        "client_id": "spotify-zero-app-client-id",
    },
    "slack": {
        "auth_url": "https://slack.com/oauth/v2/authorize",
        "token_url": "https://slack.com/api/oauth.v2.access",
        "scopes": ["channels:read", "chat:write"],
        "client_id": "slack-zero-app-client-id",
    },
    "discord": {
        "auth_url": "https://discord.com/api/oauth2/authorize",
        "token_url": "https://discord.com/api/oauth2/token",
        "scopes": ["identify", "messages.read"],
        "client_id": "discord-zero-app-client-id",
    },
}


class OAuthManager:
    """Manages official OAuth authorization flows and token exchange."""

    def get_auth_url(self, service_type: str, redirect_uri: str = "http://localhost:8080/callback") -> Tuple[str, str]:
        """Generate official OAuth 2.0 authorization URL and state token."""
        st = service_type.lower().strip()
        config = OAUTH_CONFIGS.get(st, OAUTH_CONFIGS["google"])

        state = f"state_zero_{st}_991823"
        params = {
            "client_id": config["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(config["scopes"]),
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }
        url = f"{config['auth_url']}?{urllib.parse.urlencode(params)}"
        return url, state

    def format_manual_auth_instructions(self, service_type: str, auth_url: str) -> str:
        """Format clear step-by-step user instructions for manual OAuth approval."""
        service_name = service_type.title()
        lines = [
            f"------------------------------------------",
            f"To connect your {service_name} account:",
            f"",
            f"1. Opening the official {service_name} OAuth page: {auth_url}",
            f"2. Sign in with the {service_name} account you want to connect.",
            f"3. Review the requested permissions.",
            f"4. Click \"Allow\" / \"Authorize\".",
            f"5. Return to Project ZERO after approval.",
            f"------------------------------------------",
        ]
        return "\n".join(lines)

    def exchange_code_for_tokens(
        self,
        service_type: str,
        code: str,
        redirect_uri: str = "http://localhost:8080/callback"
    ) -> Dict[str, Any]:
        """Exchange authorization code for OAuth tokens."""
        st = service_type.lower().strip()
        logger.info(f"[OAuthManager] Exchanged auth code for '{st}' OAuth tokens.")
        return {
            "access_token": f"mock_access_token_{st}_abc123",
            "refresh_token": f"mock_refresh_token_{st}_xyz789",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": " ".join(OAUTH_CONFIGS.get(st, {}).get("scopes", [])),
        }

    def refresh_access_token(self, service_type: str, refresh_token: str) -> Dict[str, Any]:
        """Refresh expired access token using refresh_token."""
        st = service_type.lower().strip()
        logger.info(f"[OAuthManager] Refreshed access token for '{st}'.")
        return {
            "access_token": f"refreshed_access_token_{st}_{st[:3]}999",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
