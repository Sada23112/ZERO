"""Project ZERO — Email Subsystem Control.

Handles email operations including sending, replying, forwarding, drafting, attachments,
and searching/reading inbox messages.
"""

import time
from typing import List, Dict, Any, Tuple, Optional
from zero_logging import logger


class EmailManager:
    """Manages email messages, inbox search, drafts, and sending."""

    def __init__(self) -> None:
        self._inbox: List[Dict[str, Any]] = [
            {
                "id": "msg-101",
                "sender": "Google Security <no-reply@google.com>",
                "subject": "Security Alert for your account",
                "body": "A new sign-in was detected on your Windows machine.",
                "timestamp": time.time() - 3600,
                "read": False,
            },
            {
                "id": "msg-102",
                "sender": "Alice Smith <alice@example.com>",
                "subject": "Project ZERO Q3 Status Report",
                "body": "Hi, please review the attached Q3 roadmap document.",
                "timestamp": time.time() - 1800,
                "read": False,
            },
            {
                "id": "msg-103",
                "sender": "Manager <manager@corp.com>",
                "subject": "Weekly Planning Meeting",
                "body": "Let's align on tomorrow's deliverables.",
                "timestamp": time.time() - 900,
                "read": True,
            },
        ]
        self._drafts: List[Dict[str, Any]] = []

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        """Send an email to specified recipient."""
        att_str = f" with attachments ({', '.join(attachments)})" if attachments else ""
        logger.info(f"[Email] Sent email to '{recipient}' | Subject: '{subject}'{att_str}")
        return True, f"Email successfully sent to {recipient}{att_str}."

    def reply_latest(self, body: str) -> Tuple[bool, str]:
        """Reply to the most recent email in inbox."""
        latest = self.read_latest()
        if not latest:
            return False, "No emails found in inbox to reply to."

        reply_subj = f"Re: {latest['subject']}"
        recipient = latest["sender"]
        return self.send_email(recipient, reply_subj, body)

    def forward_latest(self, recipient: str, comment: Optional[str] = None) -> Tuple[bool, str]:
        """Forward latest email to recipient."""
        latest = self.read_latest()
        if not latest:
            return False, "No email available to forward."

        fwd_subj = f"Fwd: {latest['subject']}"
        fwd_body = (comment or "") + f"\n\n--- Original Message ---\nFrom: {latest['sender']}\n{latest['body']}"
        return self.send_email(recipient, fwd_subj, fwd_body)

    def save_draft(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        """Create and save email draft."""
        draft = {
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "attachments": attachments or [],
            "timestamp": time.time(),
        }
        self._drafts.append(draft)
        logger.info(f"[Email] Saved draft to '{recipient}'")
        return True, f"Draft email to '{recipient}' saved successfully."

    def search_inbox(self, query: str) -> List[Dict[str, Any]]:
        """Search inbox by sender, subject, or content keyword."""
        q = query.lower().strip()
        results = []
        for msg in self._inbox:
            if q in msg["sender"].lower() or q in msg["subject"].lower() or q in msg["body"].lower():
                results.append(msg)
        return results

    def read_unread(self) -> List[Dict[str, Any]]:
        """Fetch all unread messages."""
        unread = [msg for msg in self._inbox if not msg["read"]]
        for msg in unread:
            msg["read"] = True
        return unread

    def read_latest(self) -> Dict[str, Any]:
        """Fetch latest message in inbox."""
        if self._inbox:
            latest = self._inbox[-1]
            latest["read"] = True
            return latest
        return {}

    def search_sender(self, sender: str) -> List[Dict[str, Any]]:
        """Filter inbox by sender name/address."""
        s = sender.lower().strip()
        return [msg for msg in self._inbox if s in msg["sender"].lower()]
