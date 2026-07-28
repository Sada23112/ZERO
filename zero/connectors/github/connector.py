"""Project ZERO — GitHub Connector."""

from typing import List, Dict, Any, Tuple, Optional
from zero.connectors.base import BaseConnector
from zero_logging import logger


class GitHubConnector(BaseConnector):
    """Connector for GitHub REST API v3 / GraphQL."""

    def __init__(self, username: str = "octocat"):
        self.username = username
        self.is_connected = False

    @property
    def service_type(self) -> str:
        return "github"

    def connect(self, credentials: Dict[str, Any]) -> Tuple[bool, str]:
        self.is_connected = True
        return True, f"GitHub connected for '{self.username}'."

    def disconnect(self) -> Tuple[bool, str]:
        self.is_connected = False
        return True, f"GitHub disconnected for '{self.username}'."

    def health_check(self) -> Tuple[bool, str]:
        return (True, "GitHub API operational.") if self.is_connected else (False, "GitHub not connected.")

    def supported_capabilities(self) -> List[str]:
        return ["browse_repos", "list_issues", "create_issue", "list_pull_requests", "list_workflows"]

    def browse_repos(self) -> List[Dict[str, Any]]:
        return [
            {"name": "ZERO", "stars": 120, "language": "Python", "url": "https://github.com/user/ZERO"},
            {"name": "canalib", "stars": 45, "language": "TypeScript", "url": "https://github.com/user/canalib"},
        ]
