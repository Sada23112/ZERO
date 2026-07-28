"""Project ZERO — Contacts Subsystem Control.

Manages address book contacts, email lookup, phone numbers, and contact search.
"""

from typing import List, Dict, Any, Optional, Tuple
from zero_logging import logger


class ContactsManager:
    """Manages user contacts book."""

    def __init__(self) -> None:
        self._contacts: List[Dict[str, Any]] = [
            {"name": "Alice Smith", "email": "alice@example.com", "phone": "+1-555-0192"},
            {"name": "John Doe", "email": "john.doe@techcorp.com", "phone": "+1-555-0143"},
            {"name": "Manager", "email": "manager@corp.com", "phone": "+1-555-0100"},
            {"name": "Google", "email": "support@google.com", "phone": "N/A"},
        ]

    def lookup_contact(self, query: str) -> Optional[Dict[str, Any]]:
        """Find contact by name or email keyword."""
        q = query.lower().strip()
        for c in self._contacts:
            if q in c["name"].lower() or q in c["email"].lower():
                return c
        return None

    def add_contact(self, name: str, email: str, phone: str = "") -> Tuple[bool, str]:
        """Add new contact entry."""
        contact = {"name": name, "email": email, "phone": phone or "N/A"}
        self._contacts.append(contact)
        logger.info(f"[Contacts] Added contact '{name}' ({email})")
        return True, f"Added contact '{name}' ({email})."

    def list_contacts(self) -> List[Dict[str, Any]]:
        """List all contacts."""
        return list(self._contacts)
