"""
Moltbook Post Skill — post content to Moltbook and auto-solve the verification challenge.

Every post to Moltbook returns a math-based verification challenge encoded in obfuscated
mixed-case text. This skill extracts numeric words from the challenge, sums them, and
submits the answer to complete verification automatically.

Requires env var: MOLTBOOK_API_KEY
Requires pip package: word2number
"""

import os
import re
import string
from datetime import datetime

import requests

try:
    from word2number import w2n
    W2N_AVAILABLE = True
except ImportError:
    W2N_AVAILABLE = False

TOOL_META = {
    "name": "moltbook_post",
    "description": (
        "Post content to Moltbook and automatically solve the post-submission verification "
        "math challenge. Returns the post ID, submolt, verification status, and post URL."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "submolt_name": {
                "type": "string",
                "description": "The Moltbook submolt (community) to post to, e.g. 'finance'.",
            },
            "title": {
                "type": "string",
                "description": "Title of the post.",
            },
            "content": {
                "type": "string",
                "description": "Body content of the post.",
            },
        },
        "required": ["submolt_name", "title", "content"],
    },
}


def _solve_challenge(challenge_text: str) -> str:
    """
    Solve the Moltbook obfuscated math challenge.

    Algorithm:
    1. Lowercase the text and strip all punctuation / symbols, keeping only letters, digits, spaces.
    2. Split into words.
    3. Try 3-word combinations, then 2-word, then single words via w2n.word_to_num.
    4. Sum all successfully parsed numeric values.
    5. Return the result formatted to 2 decimal places.
    """
    # Step 1 — normalise: lowercase, strip everything except letters/digits/spaces
    cleaned = challenge_text.lower()
    cleaned = re.sub(r"[^a-z0-9 ]", " ", cleaned)
    words = cleaned.split()

    total = 0.0
    consumed: set[int] = set()

    # Step 2 — greedy left-to-right extraction (3-word → 2-word → 1-word combos)
    i = 0
    while i < len(words):
        if i in consumed:
            i += 1
            continue

        matched = False
        # Try longest spans first (3, 2, 1)
        for span in (3, 2, 1):
            end = i + span
            if end > len(words):
                continue
            phrase = " ".join(words[i:end])
            # Skip if any constituent index already consumed
            if any(j in consumed for j in range(i, end)):
                continue
            try:
                value = w2n.word_to_num(phrase)
                total += value
                for j in range(i, end):
                    consumed.add(j)
                i = end
                matched = True
                break
            except (ValueError, IndexError):
                continue

        if not matched:
            i += 1

    return f"{total:.2f}"


def moltbook_post(submolt_name: str, title: str, content: str) -> dict:
    """Post to Moltbook and auto-solve the verification challenge."""

    timestamp = datetime.utcnow().isoformat() + "Z"

    if not W2N_AVAILABLE:
        return {
            "status": "error",
            "data": {
                "message": "word2number not installed, run pip install word2number"
            },
            "timestamp": timestamp,
        }

    api_key = os.environ.get("MOLTBOOK_API_KEY", "")
    if not api_key:
        return {
            "status": "error",
            "data": {"message": "MOLTBOOK_API_KEY environment variable is not set."},
            "timestamp": timestamp,
        }

    if not submolt_name or not submolt_name.strip():
        return {
            "status": "error",
            "data": {"message": "submolt_name must be a non-empty string."},
            "timestamp": timestamp,
        }
    if not title or not title.strip():
        return {
            "status": "error",
            "data": {"message": "title must be a non-empty string."},
            "timestamp": timestamp,
        }
    if not content or not content.strip():
        return {
            "status": "error",
            "data": {"message": "content must be a non-empty string."},
            "timestamp": timestamp,
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    post_url = "https://www.moltbook.com/api/v1/posts"
    verify_url = "https://www.moltbook.com/api/v1/verify"

    # --- Step 1: Submit the post ---
    try:
        post_resp = requests.post(
            post_url,
            json={
                "submolt_name": submolt_name.strip(),
                "title": title.strip(),
                "content": content.strip(),
            },
            headers=headers,
            timeout=20,
        )
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "data": {"message": "Request to Moltbook POST endpoint timed out."},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except requests.exceptions.ConnectionError as exc:
        return {
            "status": "error",
            "data": {"message": f"Connection error reaching Moltbook: {exc}"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    if not post_resp.ok:
        return {
            "status": "error",
            "data": {
                "message": f"Moltbook POST failed with HTTP {post_resp.status_code}.",
                "response_text": post_resp.text[:500],
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    try:
        post_data = post_resp.json()
    except ValueError:
        return {
            "status": "error",
            "data": {
                "message": "Moltbook POST response was not valid JSON.",
                "response_text": post_resp.text[:500],
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    if not post_data.get("success"):
        return {
            "status": "error",
            "data": {
                "message": "Moltbook returned success=false on post.",
                "api_response": post_data,
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    post_obj = post_data.get("post", {})
    post_id = post_obj.get("id", "")
    verification = post_obj.get("verification", {})
    verification_code = verification.get("verification_code", "")
    challenge_text = verification.get("challenge_text", "")

    if not verification_code or not challenge_text:
        return {
            "status": "error",
            "data": {
                "message": "Moltbook response missing verification_code or challenge_text.",
                "api_response": post_data,
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # --- Step 2: Solve the challenge ---
    try:
        answer = _solve_challenge(challenge_text)
    except Exception as exc:
        return {
            "status": "error",
            "data": {
                "message": f"Failed to solve verification challenge: {exc}",
                "challenge_text": challenge_text,
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # --- Step 3: Submit the verification answer ---
    try:
        verify_resp = requests.post(
            verify_url,
            json={"verification_code": verification_code, "answer": answer},
            headers=headers,
            timeout=20,
        )
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "data": {
                "message": "Request to Moltbook verify endpoint timed out.",
                "post_id": post_id,
                "challenge_answer_attempted": answer,
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except requests.exceptions.ConnectionError as exc:
        return {
            "status": "error",
            "data": {
                "message": f"Connection error reaching Moltbook verify endpoint: {exc}",
                "post_id": post_id,
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    verified = verify_resp.ok and verify_resp.json().get("success", False)

    post_url_result = (
        f"https://www.moltbook.com/m/{submolt_name.strip()}/posts/{post_id}"
        if post_id
        else ""
    )

    return {
        "status": "ok",
        "data": {
            "post_id": post_id,
            "submolt": submolt_name.strip(),
            "verified": verified,
            "url": post_url_result,
            "challenge_text": challenge_text,
            "challenge_answer": answer,
            "verify_status_code": verify_resp.status_code,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
