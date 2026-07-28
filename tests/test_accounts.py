"""Project ZERO — Unit Tests for Phase 10 Connected Accounts & External Services."""

import pytest
import os
from zero.accounts.credential_store import EncryptedCredentialStore
from zero.accounts.account_registry import AccountRegistry, ConnectedAccount
from zero.accounts.oauth_manager import OAuthManager
from zero.accounts.permission_manager import AccountPermissionManager
from zero.accounts.account_preferences import AccountPreferences
from zero.accounts.service_discovery import ServiceDiscovery
from zero.accounts.connector_loader import ConnectorLoader
from zero.accounts.account_manager import AccountManager


def test_credential_store_encryption():
    store = EncryptedCredentialStore()
    store.save_credentials("test_acct_1", {"access_token": "secret_token_123", "refresh_token": "ref_456"})

    creds = store.load_credentials("test_acct_1")
    assert creds is not None
    assert creds["access_token"] == "secret_token_123"
    assert creds["refresh_token"] == "ref_456"

    masked = EncryptedCredentialStore.mask_secret("secret_token_123")
    assert "..." in masked
    assert "secret" not in masked

    deleted = store.delete_credentials("test_acct_1")
    assert deleted is True


def test_account_registry():
    registry = AccountRegistry()
    acct = ConnectedAccount(
        account_id="google_work_test",
        service_type="google",
        email="work@company.com",
        display_name="Work Gmail",
        account_category="work"
    )
    registry.register_account(acct)

    fetched = registry.get_account("google_work_test")
    assert fetched is not None
    assert fetched.email == "work@company.com"

    list_accts = registry.get_accounts_by_service("google")
    assert len(list_accts) >= 1

    registry.unregister_account("google_work_test")


def test_oauth_manager():
    oauth = OAuthManager()
    url, state = oauth.get_auth_url("google")
    assert "accounts.google.com" in url
    assert "scope=" in url

    instructions = oauth.format_manual_auth_instructions("google", url)
    assert "To connect your Google account:" in instructions
    assert "Sign in" in instructions
    assert "Click \"Allow\"" in instructions

    tokens = oauth.exchange_code_for_tokens("google", "test_code")
    assert "access_token" in tokens
    assert "refresh_token" in tokens


def test_account_permission_manager():
    perms = AccountPermissionManager()
    auth1, _ = perms.check_permission("read_calendar", "user@gmail.com")
    assert auth1 is True

    auth2, _ = perms.check_permission("send_email", "user@gmail.com")
    assert auth2 is True

    auth3, _ = perms.check_permission("delete_drive_file", "user@gmail.com")
    assert auth3 is True


def test_account_preferences():
    prefs = AccountPreferences()
    prefs.set_preference("work", "work@company.com")
    assert prefs.get_preference("work") == "work@company.com"


def test_service_discovery():
    discovery = ServiceDiscovery()
    accounts = discovery.discover_browser_accounts()
    assert len(accounts) >= 1
    prompt = discovery.format_discovery_prompt("google")
    assert "accounts in Chrome" in prompt


def test_connectors():
    loader = ConnectorLoader()

    gmail = loader.get_connector("gmail")
    assert gmail is not None
    succ, _ = gmail.connect({"token": "abc"})
    assert succ is True
    inbox = gmail.read_inbox()
    assert len(inbox) >= 1

    github = loader.get_connector("github")
    assert github is not None
    repos = github.browse_repos()
    assert len(repos) >= 1

    spotify = loader.get_connector("spotify")
    assert spotify is not None
    assert "play_playback" in spotify.supported_capabilities()


def test_account_manager_end_to_end():
    mgr = AccountManager()

    # 1. Natural language connection request returns manual OAuth instructions
    res = mgr.process_account_command("Connect my Google account")
    assert "[Phase 10 Connected Accounts]" in res
    assert "1. Opening the official Google OAuth page" in res

    # 2. Complete connection for Personal & Work Gmail
    mgr.complete_connection("google", "personal@gmail.com", account_category="personal")
    mgr.complete_connection("google", "work@company.com", account_category="work")

    # 3. Disambiguation when multiple accounts exist and no preference is set
    mgr.preferences.clear_preferences()
    acct, prompt = mgr.resolve_account_for_task("google", ignore_preference=True)
    assert acct is None
    assert "I found 2 Google accounts connected:" in prompt

    # 4. Resolve using preference hint
    acct_work, _ = mgr.resolve_account_for_task("google", category_hint="work")
    assert acct_work is not None
    assert acct_work.email == "work@company.com"

    # 5. Persistent Session Restoration & Automatic Token Refresh (No re-login required)
    connector, msg = mgr.get_connector_for_account("personal@gmail.com")
    assert connector is not None
    assert "Active session restored" in msg
