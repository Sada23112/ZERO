"""Project ZERO — Connected Accounts & External Services Package.

Provides encrypted credential storage, account profiles, official OAuth 2.0 flows,
service connectors, permission enforcement, multi-account management, and preferences.
"""

from zero.accounts.credential_store import EncryptedCredentialStore
from zero.accounts.account_registry import AccountRegistry, ConnectedAccount
from zero.accounts.oauth_manager import OAuthManager
from zero.accounts.permission_manager import AccountPermissionManager
from zero.accounts.account_preferences import AccountPreferences
from zero.accounts.service_discovery import ServiceDiscovery
from zero.accounts.connector_loader import ConnectorLoader
from zero.accounts.account_manager import AccountManager, account_manager

__all__ = [
    "EncryptedCredentialStore",
    "AccountRegistry",
    "ConnectedAccount",
    "OAuthManager",
    "AccountPermissionManager",
    "AccountPreferences",
    "ServiceDiscovery",
    "ConnectorLoader",
    "AccountManager",
    "account_manager",
]
