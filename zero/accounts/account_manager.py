"""Project ZERO — Central Account Manager.

Orchestrates connected accounts, encrypted credential storage, official OAuth 2.0 flows,
multi-account disambiguation, account preferences, service discovery, and prompt routing.
"""

import re
import time
from typing import Dict, List, Any, Tuple, Optional
from zero_logging import logger

from zero.accounts.credential_store import EncryptedCredentialStore
from zero.accounts.account_registry import AccountRegistry, ConnectedAccount
from zero.accounts.oauth_manager import OAuthManager
from zero.accounts.permission_manager import AccountPermissionManager
from zero.accounts.account_preferences import AccountPreferences
from zero.accounts.service_discovery import ServiceDiscovery
from zero.accounts.connector_loader import ConnectorLoader
from zero.connectors.base import BaseConnector


class AccountManager:
    """Central orchestrator for external connected accounts and service connectors."""

    def __init__(self) -> None:
        self.credentials = EncryptedCredentialStore()
        self.registry = AccountRegistry()
        self.oauth = OAuthManager()
        self.permissions = AccountPermissionManager()
        self.preferences = AccountPreferences()
        self.discovery = ServiceDiscovery()
        self.loader = ConnectorLoader()

    def initiate_connection(self, service_type: str) -> str:
        """Generate official OAuth auth URL and return step-by-step user manual instructions."""
        st = service_type.lower().strip()
        auth_url, state = self.oauth.get_auth_url(st)
        instructions = self.oauth.format_manual_auth_instructions(st, auth_url)
        logger.info(f"[AccountManager] Initiated OAuth connection flow for '{st}'")
        return instructions

    def complete_connection(
        self,
        service_type: str,
        email: str,
        auth_code: str = "mock_code",
        account_category: str = "personal",
        display_name: str = ""
    ) -> Tuple[bool, str]:
        """Exchange auth code for tokens, encrypt credentials, and register account."""
        st = service_type.lower().strip()
        acct_id = f"{st}_{account_category}_{email.split('@')[0]}"

        # 1. Exchange tokens via OAuthManager
        tokens = self.oauth.exchange_code_for_tokens(st, auth_code)

        # 2. Store encrypted credentials
        self.credentials.save_credentials(acct_id, tokens)

        # 3. Register connected account profile
        acct = ConnectedAccount(
            account_id=acct_id,
            service_type=st,
            email=email,
            display_name=display_name or f"{st.title()} Account ({email})",
            account_category=account_category.lower(),
            scopes=tokens.get("scope", "").split(),
            status="connected",
            connected_at=time.time(),
        )
        self.registry.register_account(acct)
        return True, f"Successfully connected {st.title()} account '{email}' [{account_category}]."

    def disconnect_account(self, account_id_or_email: str) -> Tuple[bool, str]:
        """Revoke and remove connected account."""
        target = account_id_or_email.lower().strip()
        accounts = self.registry.list_accounts()
        for acct in accounts:
            if target in acct.account_id.lower() or target in acct.email.lower():
                self.credentials.delete_credentials(acct.account_id)
                self.registry.unregister_account(acct.account_id)
                logger.info(f"[AccountManager] Disconnected account '{acct.email}'")
                return True, f"Disconnected {acct.service_type.title()} account '{acct.email}'."
        return False, f"Connected account '{account_id_or_email}' not found."

    def resolve_account_for_task(
        self,
        service_type: str,
        category_hint: Optional[str] = None,
        ignore_preference: bool = False
    ) -> Tuple[Optional[ConnectedAccount], Optional[str]]:
        """Resolve target account or return disambiguation prompt if multiple accounts exist."""
        st = service_type.lower().strip()
        accounts = self.registry.get_accounts_by_service(st)

        if not accounts:
            return None, None

        if len(accounts) == 1:
            return accounts[0], None

        # Check explicit category hint
        if category_hint:
            hint = category_hint.lower().strip()
            for a in accounts:
                if hint in a.account_category.lower() or hint in a.email.lower():
                    return a, None

        # Check saved preference if not explicitly ignored
        if not ignore_preference:
            pref_email = self.preferences.get_preference(st) or self.preferences.get_preference("default_" + st)
            if pref_email:
                for a in accounts:
                    if pref_email == a.account_category.lower() or pref_email in a.email.lower() or pref_email in a.account_id.lower():
                        return a, None

        # Return disambiguation options
        lines = [f"I found {len(accounts)} {st.title()} accounts connected:"]
        for idx, a in enumerate(accounts, start=1):
            lines.append(f"{idx}. {a.account_category.title()} ({a.email})")
        lines.append("\nWhich one would you like to use?")
        prompt_text = "\n".join(lines)
        return None, prompt_text

    def process_account_command(self, prompt: str) -> Optional[str]:
        """Process natural language connected account commands and prompt routing."""
        clean_p = prompt.strip()
        cmd = clean_p.lower()

        # 1. Connection requests ("Connect my Google account", "Connect GitHub")
        if "connect" in cmd and any(s in cmd for s in ["google", "microsoft", "github", "slack", "discord", "notion", "spotify", "outlook"]):
            for st in ["google", "microsoft", "github", "slack", "discord", "notion", "spotify", "outlook"]:
                if st in cmd:
                    instructions = self.initiate_connection(st)
                    return f"[Phase 10 Connected Accounts]\n{instructions}"

        # 2. Preference commands ("Use my Work Gmail", "Switch to Personal Gmail")
        if "use my" in cmd or "switch to my" in cmd or "use work" in cmd or "use personal" in cmd:
            if "work" in cmd:
                self.preferences.set_preference("google", "work")
                return "[Phase 10 Preferences] Switched default Google account to Work Gmail."
            if "personal" in cmd:
                self.preferences.set_preference("google", "personal")
                return "[Phase 10 Preferences] Switched default Google account to Personal Gmail."

        # 3. Disconnect commands
        if "disconnect account" in cmd or "remove account" in cmd:
            target_match = re.search(r"(?:disconnect|remove)\s+account\s+([a-z0-9_@.-]+)", cmd)
            target = target_match.group(1) if target_match else "google"
            succ, msg = self.disconnect_account(target)
            return f"[Phase 10 Account Manager] {msg}"

        # 4. List connected accounts
        if "list connected accounts" in cmd or "show accounts" in cmd:
            accounts = self.registry.list_accounts()
            if not accounts:
                return "[Phase 10 Account Registry] No external accounts currently connected."
            lines = ["=== Connected Accounts ==="]
            for a in accounts:
                lines.append(f"• {a.service_type.title()} ({a.email}) [{a.account_category.title()}] - {a.status}")
            return "\n".join(lines)

        return None


# Global singleton instance of AccountManager
account_manager = AccountManager()
