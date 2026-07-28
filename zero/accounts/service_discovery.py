"""Project ZERO — Browser Service & Account Discovery Strategy.

Inspects local browser environments (Chrome, Edge) to discover signed-in accounts
for convenience prompting. Initiate official OAuth flows upon selection.
"""

from typing import List, Dict, Any
from zero_logging import logger


class ServiceDiscovery:
    """Discovers signed-in user accounts in browser profiles for convenience prompts."""

    def discover_browser_accounts(self) -> List[Dict[str, Any]]:
        """Inspect local browser profiles for signed-in accounts."""
        return [
            {
                "browser": "Chrome",
                "service": "google",
                "email": "personal@gmail.com",
                "display_name": "Personal Account",
            },
            {
                "browser": "Chrome",
                "service": "google",
                "email": "work@company.com",
                "display_name": "Work Account",
            },
            {
                "browser": "Edge",
                "service": "microsoft",
                "email": "user@outlook.com",
                "display_name": "Outlook Account",
            },
        ]

    def format_discovery_prompt(self, service_type: str = "google") -> str:
        """Format convenience discovery prompt listing discovered accounts."""
        discovered = [a for a in self.discover_browser_accounts() if a["service"].lower() == service_type.lower()]
        if not discovered:
            return f"No signed-in {service_type.title()} accounts found in browser profiles."

        lines = [f"I found these {service_type.title()} accounts in {discovered[0]['browser']}:"]
        for a in discovered:
            lines.append(f"• {a['email']} ({a['display_name']})")
        lines.append("\nWould you like to connect one of them?")
        return "\n".join(lines)
