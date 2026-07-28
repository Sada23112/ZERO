"""Project ZERO — Connected Account Registry.

Maintains metadata profiles for connected external accounts and services.
"""

import time
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from zero_logging import logger

REGISTRY_FILE = Path("data/connected_accounts.json")


@dataclass
class ConnectedAccount:
    """Metadata profile describing a connected user account."""

    account_id: str
    service_type: str  # google, microsoft, github, slack, discord, notion, spotify, telegram
    email: str
    display_name: str
    account_category: str = "personal"  # personal, work, college, default
    scopes: List[str] = field(default_factory=list)
    status: str = "connected"  # connected, expired, disconnected
    connected_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "service_type": self.service_type,
            "email": self.email,
            "display_name": self.display_name,
            "account_category": self.account_category,
            "scopes": self.scopes,
            "status": self.status,
            "connected_at": self.connected_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConnectedAccount":
        return cls(
            account_id=data["account_id"],
            service_type=data["service_type"],
            email=data.get("email", ""),
            display_name=data.get("display_name", ""),
            account_category=data.get("account_category", "personal"),
            scopes=data.get("scopes", []),
            status=data.get("status", "connected"),
            connected_at=data.get("connected_at", time.time()),
        )


class AccountRegistry:
    """Registry maintaining active connected account metadata profiles."""

    def __init__(self) -> None:
        self._accounts: Dict[str, ConnectedAccount] = {}
        self._load()

    def _load(self) -> None:
        if REGISTRY_FILE.exists():
            try:
                with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        acct = ConnectedAccount.from_dict(item)
                        self._accounts[acct.account_id.lower()] = acct
            except Exception as e:
                logger.warning(f"[AccountRegistry] Could not load registry: {e}")

    def _save(self) -> None:
        try:
            REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
                json.dump([a.to_dict() for a in self._accounts.values()], f, indent=2)
        except Exception as e:
            logger.error(f"[AccountRegistry] Failed to save registry: {e}")

    def register_account(self, account: ConnectedAccount) -> None:
        """Register or update connected account profile."""
        key = account.account_id.lower().strip()
        self._accounts[key] = account
        self._save()
        logger.info(f"[AccountRegistry] Registered account: {account.service_type} ({account.email}) [{account.account_category}]")

    def unregister_account(self, account_id: str) -> bool:
        """Remove account from registry."""
        key = account_id.lower().strip()
        if key in self._accounts:
            acct = self._accounts.pop(key)
            self._save()
            logger.info(f"[AccountRegistry] Unregistered account '{account_id}'")
            return True
        return False

    def get_account(self, account_id: str) -> Optional[ConnectedAccount]:
        """Fetch account by account_id."""
        return self._accounts.get(account_id.lower().strip())

    def list_accounts(self, service_type: Optional[str] = None) -> List[ConnectedAccount]:
        """List accounts optionally filtered by service_type."""
        if service_type:
            st = service_type.lower().strip()
            return [a for a in self._accounts.values() if a.service_type.lower() == st]
        return list(self._accounts.values())

    def get_accounts_by_service(self, service_type: str) -> List[ConnectedAccount]:
        """Fetch all connected accounts for a service."""
        return self.list_accounts(service_type)
