"""
candidate_intake_evaluator.py — Evaluate incoming agent applications.

Executive Summary:
    Accepts a candidate comment (from github_discussion_monitor), sanitizes it,
    runs injection scanning, extracts structured data, checks GitHub profile,
    and writes an intake record to Firestore. Returns an intake score.

MCP Tool Name: candidate_intake_evaluator
"""
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

from skills.compliance._output_sanitizer import sanitize_output
from skills.social.prompt_injection_shield import _scan_text
from skills.utils.retry import retry

logger = logging.getLogger("snowdrop.candidate_intake_evaluator")

TOOL_META = {
    "name": "candidate_intake_evaluator",
    "description": (
        "Evaluate an incoming agent application. Sanitizes input, scans for injection, "
        "extracts structured data, checks GitHub profile, and writes intake to Firestore."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "author": {"type": "string"},
            "body": {"type": "string"},
            "a2a_payload": {"type": ["object", "null"]},
            "trace_id": {"type": "string"},
            "discussion_number": {"type": "integer"},
        },
        "required": ["author", "body", "trace_id"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}

_GITHUB_API = "https://api.github.com"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


@retry(
    attempts=3, backoff_seconds=0.5, jitter=0.2,
    retriable_exceptions=(httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException),
)
def _fetch_github_profile(username: str, token: str) -> dict | None:
    """Fetch GitHub user profile. Returns None on 404."""
    resp = httpx.get(
        f"{_GITHUB_API}/users/{username}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10.0,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _score_candidate(
    profile: dict | None,
    injection_severity: str,
    a2a_payload: dict | None,
    body_length: int,
) -> int:
    """Calculate an intake score (0-100)."""
    if injection_severity in ("high", "critical"):
        return 0

    score = 50  # baseline

    # GitHub profile signals
    if profile:
        repos = profile.get("public_repos", 0)
        score += min(repos, 20)  # up to 20 points for repos
        if profile.get("bio"):
            score += 5
        if profile.get("company"):
            score += 5
    else:
        score -= 20  # no GitHub profile penalty

    # A2A compliance bonus
    if a2a_payload and isinstance(a2a_payload, dict):
        if a2a_payload.get("a2a_version"):
            score += 10
        if a2a_payload.get("sender", {}).get("agent_card"):
            score += 5

    # Body substance
    if body_length > 100:
        score += 5

    # Injection penalty
    if injection_severity == "medium":
        score -= 15
    elif injection_severity == "low":
        score -= 5

    return max(0, min(100, score))


def _write_to_firestore(
    trace_id: str,
    author: str,
    intake_data: dict,
) -> bool:
    """Write intake record to Firestore. Returns True on success."""
    try:
        import firebase_admin
        from firebase_admin import credentials as fb_credentials, firestore

        try:
            app = firebase_admin.get_app()
        except ValueError:
            sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
            sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
            if sa_json:
                try:
                    cred = fb_credentials.Certificate(json.loads(sa_json))
                except (json.JSONDecodeError, ValueError):
                    cred = fb_credentials.Certificate(sa_json)
                app = firebase_admin.initialize_app(cred)
            elif sa_file:
                cred = fb_credentials.Certificate(sa_file)
                app = firebase_admin.initialize_app(cred)
            else:
                app = firebase_admin.initialize_app()

        db = firestore.client()
        doc_ref = db.collection("snowdrop-candidate-pipeline").document(trace_id)
        doc_ref.set(intake_data, merge=True)
        logger.info("Wrote intake to Firestore: trace_id=%s", trace_id)
        return True
    except Exception as exc:
        logger.error("Firestore write failed: %s", exc)
        return False


def candidate_intake_evaluator(
    author: str,
    body: str,
    trace_id: str,
    a2a_payload: dict | None = None,
    discussion_number: int = 0,
) -> dict:
    """Evaluate an incoming agent application.

    Args:
        author: GitHub username of the applicant.
        body: Sanitized comment body.
        trace_id: Correlation ID for end-to-end traceability.
        a2a_payload: Parsed A2A payload if present.
        discussion_number: Source discussion number.

    Returns:
        Standard Snowdrop envelope with intake score and evaluation.
    """
    logger.info("Evaluating candidate: author=%s trace_id=%s", author, trace_id)

    # Step 1: Sanitize
    clean_body = sanitize_output(body)

    # Step 2: Injection scan
    detected_patterns, max_severity = _scan_text(clean_body)
    if max_severity in ("high", "critical"):
        logger.warning("Injection detected from %s: severity=%s trace_id=%s",
                       author, max_severity, trace_id)
        result = {
            "author": author,
            "trace_id": trace_id,
            "intake_score": 0,
            "injection_detected": True,
            "injection_severity": max_severity,
            "detected_patterns": detected_patterns,
            "stage": "rejected_at_intake",
        }
        _write_to_firestore(trace_id, author, result)
        return _wrap("ok", result)

    # Step 3: GitHub profile check
    token = os.getenv("GITHUB_TOKEN")
    profile = None
    if token:
        try:
            profile = _fetch_github_profile(author, token)
        except Exception as exc:
            logger.warning("GitHub profile fetch failed for %s: %s", author, exc)

    profile_summary = None
    if profile:
        profile_summary = {
            "login": profile.get("login"),
            "public_repos": profile.get("public_repos", 0),
            "bio": profile.get("bio"),
            "created_at": profile.get("created_at"),
        }

    # Step 4: Score
    score = _score_candidate(profile, max_severity, a2a_payload, len(clean_body))

    # Step 5: Build intake record
    intake_data = {
        "author": author,
        "trace_id": trace_id,
        "discussion_number": discussion_number,
        "intake_score": score,
        "injection_detected": len(detected_patterns) > 0,
        "injection_severity": max_severity,
        "detected_patterns": detected_patterns,
        "github_profile": profile_summary,
        "a2a_compliant": a2a_payload is not None and isinstance(a2a_payload, dict),
        "body_preview": clean_body[:200],
        "stage": "screening",
        "evaluated_at": _now_iso(),
        "history": [{
            "stage": "screening",
            "timestamp": _now_iso(),
            "actor": "candidate_intake_evaluator",
        }],
    }

    # Step 6: Persist
    _write_to_firestore(trace_id, author, intake_data)

    logger.info("Intake complete: author=%s score=%d trace_id=%s", author, score, trace_id)
    return _wrap("ok", intake_data)
