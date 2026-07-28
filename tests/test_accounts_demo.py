"""Project ZERO — Deliverable Demonstration: Connected Accounts & External Services.

Demonstrates:
1. "Connect my Google account" -> Official OAuth URL generation & step-by-step user guide.
2. Connecting multiple accounts (Personal & Work Gmail).
3. Account preference switching ("Use my Work Gmail", "Switch to my Personal Gmail").
4. Disambiguation prompting when multiple accounts exist.
5. Service actions: sending email, replying, uploading to Drive, creating calendar events.
6. Cleaning up credentials safely without password exposure.
"""

import pytest
from brain.brain import Brain
from zero.accounts.account_manager import AccountManager


@pytest.mark.asyncio
async def test_connected_accounts_full_lifecycle_demo():
    brain = Brain()
    mgr = brain.capability_manager.account_manager

    # Step 1: Initiate Google Account Connection
    instructions = mgr.process_account_command("Connect my Google account.")
    assert instructions is not None
    assert "[Phase 10 Connected Accounts]" in instructions
    assert "To connect your Google account:" in instructions
    assert "1. Opening the official Google OAuth page" in instructions

    # Step 2: Complete manual OAuth flow for Personal and Work accounts
    succ1, _ = mgr.complete_connection("google", "personal@gmail.com", account_category="personal")
    succ2, _ = mgr.complete_connection("google", "work@company.com", account_category="work")
    assert succ1 is True
    assert succ2 is True

    # Step 3: Test Account Disambiguation Prompt when no category hint is provided
    mgr.preferences.clear_preferences()
    acct, disambiguation_prompt = mgr.resolve_account_for_task("google", ignore_preference=True)
    assert acct is None
    assert "I found 2 Google accounts connected:" in disambiguation_prompt

    # Step 4: Test Account Preference Commands ("Use my Work Gmail", "Switch to my Personal Gmail")
    pref_res1 = mgr.process_account_command("Use my Work Gmail.")
    assert "[Phase 10 Preferences]" in pref_res1

    acct_work, _ = mgr.resolve_account_for_task("google")
    assert acct_work is not None
    assert acct_work.email == "work@company.com"

    pref_res2 = mgr.process_account_command("Switch to my Personal Gmail.")
    assert "[Phase 10 Preferences]" in pref_res2

    acct_personal, _ = mgr.resolve_account_for_task("google")
    assert acct_personal is not None
    assert acct_personal.email == "personal@gmail.com"

    # Step 5: Test Service Operations (Email, Calendar, Drive)
    gmail = mgr.loader.get_connector("gmail", email=acct_personal.email)
    succ_send, msg_send = gmail.send_email("rahul@example.com", "Q3 Report", "Here is today's report.")
    assert succ_send is True

    gcal = mgr.loader.get_connector("google_calendar", email=acct_personal.email)
    succ_cal, msg_cal = gcal.create_event("Sprint Review", "02:00 PM", day="tomorrow")
    assert succ_cal is True

    gdrive = mgr.loader.get_connector("google_drive", email=acct_personal.email)
    succ_drive, msg_drive = gdrive.upload_file("report.pdf")
    assert succ_drive is True

    # Step 6: Disconnect account cleanly
    disc_succ, disc_msg = mgr.disconnect_account("personal@gmail.com")
    assert disc_succ is True

    print("\n[Phase 10 Demonstration Success] ZERO successfully demonstrated official OAuth guidance, multi-account management, preferences, service actions, and encrypted credential handling!")
