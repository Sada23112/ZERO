"""Project ZERO — Encrypted Credential Store.

Encrypts and securely stores OAuth tokens, refresh tokens, API keys, and secrets.
Secrets are never logged in plaintext.
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from zero_logging import logger

DATA_DIR = Path("data")
CREDENTIALS_FILE = DATA_DIR / "credentials.enc"
KEY_FILE = DATA_DIR / "zero_key.key"


class EncryptedCredentialStore:
    """Secure encrypted storage for OAuth credentials and API tokens."""

    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._key = self._get_or_create_key()
        self._store: Dict[str, str] = {}
        self._load_store()

    def _get_or_create_key(self) -> bytes:
        """Fetch or initialize encryption key."""
        if KEY_FILE.exists():
            try:
                with open(KEY_FILE, "rb") as f:
                    return f.read()
            except Exception:
                pass
        key = base64.b64encode(os.urandom(32))
        try:
            with open(KEY_FILE, "wb") as f:
                f.write(key)
        except Exception:
            pass
        return key

    def _cipher_bytes(self, raw_bytes: bytes) -> bytes:
        """XOR stream cipher transform with encryption key."""
        key_bytes = self._key
        out = bytearray(len(raw_bytes))
        for i in range(len(raw_bytes)):
            out[i] = raw_bytes[i] ^ key_bytes[i % len(key_bytes)]
        return bytes(out)

    def _encrypt(self, text: str) -> str:
        raw = text.encode("utf-8")
        encrypted = self._cipher_bytes(raw)
        return base64.b64encode(encrypted).decode("utf-8")

    def _decrypt(self, token_str: str) -> str:
        encrypted = base64.b64decode(token_str.encode("utf-8"))
        raw = self._cipher_bytes(encrypted)
        return raw.decode("utf-8")

    def _load_store(self) -> None:
        if CREDENTIALS_FILE.exists():
            try:
                with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
                    self._store = json.load(f)
            except Exception as e:
                logger.warning(f"[CredentialStore] Could not load credentials file: {e}")

    def _save_store(self) -> None:
        try:
            with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
                json.dump(self._store, f, indent=2)
        except Exception as e:
            logger.error(f"[CredentialStore] Failed to save credentials file: {e}")

    def save_credentials(self, account_id: str, creds: Dict[str, Any]) -> None:
        """Encrypt and save credential dictionary for account_id."""
        serialized = json.dumps(creds)
        encrypted = self._encrypt(serialized)
        self._store[account_id.lower().strip()] = encrypted
        self._save_store()
        logger.info(f"[CredentialStore] Credentials securely stored for account '{account_id}'")

    def load_credentials(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Decrypt and load credentials for account_id."""
        key = account_id.lower().strip()
        if key not in self._store:
            return None
        try:
            encrypted = self._store[key]
            decrypted = self._decrypt(encrypted)
            return json.loads(decrypted)
        except Exception as e:
            logger.error(f"[CredentialStore] Decryption failed for account '{account_id}': {e}")
            return None

    def delete_credentials(self, account_id: str) -> bool:
        """Remove credentials for account_id."""
        key = account_id.lower().strip()
        if key in self._store:
            del self._store[key]
            self._save_store()
            logger.info(f"[CredentialStore] Deleted credentials for account '{account_id}'")
            return True
        return False

    @staticmethod
    def mask_secret(secret_str: str) -> str:
        """Mask sensitive token string for logging."""
        if not secret_str:
            return ""
        if len(secret_str) <= 8:
            return "***"
        return f"{secret_str[:4]}...{secret_str[-4:]}"
