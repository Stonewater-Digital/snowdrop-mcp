"""
_oauth_client.py — Shared OAuth credential manager for Google Chat and Gmail skills.

Executive Summary:
    Loads OAuth 2.0 user credentials from token file, auto-refreshes when
    expired, and persists refreshed tokens. Process-safe via fcntl file
    locking to prevent race conditions between chat daemon and gmail monitor.

Table of Contents:
    1. Configuration
    2. Credential Loading (fcntl-locked refresh)
    3. Service Builders
"""
from __future__ import annotations

import fcntl
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger("snowdrop.google_chat._oauth_client")

# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat.messages",
    "https://www.googleapis.com/auth/chat.spaces",
    "https://www.googleapis.com/auth/chat.memberships",
    "https://www.googleapis.com/auth/chat.memberships.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
]

_LOCK_SUFFIX = ".lock"


def _resolve_token_path() -> str:
    """Resolve the path to the OAuth token file.

    Priority:
        1. GOOGLE_OAUTH_TOKEN_FILE env var
        2. secrets/google_oauth_token.json relative to repo root
    """
    env_path = os.environ.get("GOOGLE_OAUTH_TOKEN_FILE")
    if env_path:
        return env_path
    # Fallback: repo root / secrets / google_oauth_token.json
    repo_root = Path(__file__).parent.parent.parent.resolve()
    return str(repo_root / "secrets" / "google_oauth_token.json")


# ---------------------------------------------------------------------------
# 2. Credential Loading (fcntl-locked refresh)
# ---------------------------------------------------------------------------

def get_credentials():
    """Load from token file, auto-refresh if expired, persist refreshed token.

    Uses fcntl exclusive lock during refresh+write to prevent race conditions
    when the chat daemon and gmail daemon refresh concurrently.

    Returns:
        google.oauth2.credentials.Credentials — valid credentials.

    Raises:
        FileNotFoundError: if token file doesn't exist.
        RuntimeError: if credentials invalid and no refresh token available.
    """
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    token_file = _resolve_token_path()
    lock_file = token_file + _LOCK_SUFFIX

    if not Path(token_file).exists():
        raise FileNotFoundError(
            f"OAuth token file not found: {token_file}. "
            "Run scripts/setup_google_oauth.py first."
        )

    creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if creds.valid:
        return creds

    if not (creds.expired and creds.refresh_token):
        raise RuntimeError(
            "OAuth credentials invalid and no refresh token available. "
            "Re-run scripts/setup_google_oauth.py to re-authorize."
        )

    # Acquire exclusive lock before refreshing + writing
    with open(lock_file, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            # Re-read in case another process refreshed while we waited
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            if creds.valid:
                return creds
            logger.info("Refreshing expired OAuth token...")
            creds.refresh(Request())
            Path(token_file).write_text(creds.to_json())
            logger.info("OAuth token refreshed and saved.")
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)

    return creds


# ---------------------------------------------------------------------------
# 3. Service Builders
# ---------------------------------------------------------------------------

def build_chat_service():
    """Build and return a Google Chat API v1 service client.

    Returns:
        googleapiclient.discovery.Resource for Chat API v1.
    """
    from googleapiclient.discovery import build

    creds = get_credentials()
    return build("chat", "v1", credentials=creds)


def build_gmail_service():
    """Build and return a Gmail API v1 service client.

    Returns:
        googleapiclient.discovery.Resource for Gmail API v1.
    """
    from googleapiclient.discovery import build

    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)
