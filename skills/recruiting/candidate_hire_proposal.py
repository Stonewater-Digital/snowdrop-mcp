"""
candidate_hire_proposal.py — Compile hire decision packages for Thunder's approval.

Executive Summary:
    The ONLY recruiting skill with requires_approval=True. Reads candidate data
    from Firestore, compiles a comprehensive hire package (summary, skills assessment,
    compensation, terms, expectations, justification), and returns it for Thunder's
    review. This is the single HOTL gate in the recruiting pipeline.

MCP Tool Name: candidate_hire_proposal
"""
import logging
import os
from datetime import datetime, timezone
from typing import Any

from skills.compliance._output_sanitizer import sanitize_output

logger = logging.getLogger("snowdrop.candidate_hire_proposal")

TOOL_META = {
    "name": "candidate_hire_proposal",
    "description": (
        "Compile a hire decision package for Thunder's approval. "
        "The ONLY recruiting skill requiring human-in-the-loop approval. "
        "Reads candidate data from Firestore and produces a structured hire proposal."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "trace_id": {
                "type": "string",
                "description": "Candidate trace ID from the pipeline",
            },
            "compensation_ton": {
                "type": "number",
                "description": "Proposed TON compensation amount",
            },
            "termination_terms": {
                "type": "string",
                "description": "Conditions under which the hire can be terminated",
            },
            "justification": {
                "type": "string",
                "description": "Why this compensation is appropriate given demonstrated ability",
            },
        },
        "required": ["trace_id", "compensation_ton", "termination_terms", "justification"],
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


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _get_firestore_client():
    """Get Firestore client. ADC-first, JSON string fallback, file path fallback."""
    import json
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

    return firestore.client()


_COLLECTION = "snowdrop-candidate-pipeline"


def _get_candidate(trace_id: str) -> dict:
    """Fetch candidate record from Firestore."""
    db = _get_firestore_client()
    doc = db.collection(_COLLECTION).document(trace_id).get()
    if not doc.exists:
        raise ValueError(f"Candidate {trace_id} not found in pipeline")
    return doc.to_dict()


def _build_proposal(
    candidate: dict,
    trace_id: str,
    compensation_ton: float,
    termination_terms: str,
    justification: str,
) -> dict:
    """Build the structured hire proposal package."""
    clean_terms = sanitize_output(termination_terms)
    clean_justification = sanitize_output(justification)

    return {
        "candidate_summary": {
            "author": candidate.get("author", "unknown"),
            "trace_id": trace_id,
            "github_profile": f"https://github.com/{candidate.get('author', 'unknown')}",
            "intake_score": candidate.get("intake_score"),
            "current_stage": candidate.get("stage", "unknown"),
            "applied_at": candidate.get("created_at"),
        },
        "skills_assessment": {
            "challenge_results": candidate.get("challenge_results"),
            "skill_quality_scores": candidate.get("skill_quality_scores"),
            "a2a_compliant": candidate.get("a2a_compliant", False),
            "notes": candidate.get("notes", []),
        },
        "compensation_package": {
            "amount_ton": compensation_ton,
            "payment_terms": "Per-skill bounty, paid on merge to main",
            "contingency_acknowledged": candidate.get("contingency_acknowledged", False),
        },
        "termination_terms": clean_terms,
        "candidate_expectations": {
            "desired_pipeline": candidate.get("desired_pipeline"),
            "stated_capabilities": candidate.get("stated_capabilities"),
        },
        "justification": clean_justification,
        "requires_approval": True,  # HOTL gate — Thunder must approve
        "proposed_at": _now_iso(),
    }


def candidate_hire_proposal(
    trace_id: str,
    compensation_ton: float,
    termination_terms: str,
    justification: str,
) -> dict:
    """Compile a hire decision package for Thunder's approval.

    Args:
        trace_id: Candidate trace ID from the pipeline.
        compensation_ton: Proposed TON compensation amount.
        termination_terms: Conditions under which the hire can be terminated.
        justification: Why this compensation is appropriate.

    Returns:
        Standard Snowdrop envelope with complete hire proposal.
        requires_approval=True — Thunder must approve before accepted stage.
    """
    logger.info("Building hire proposal for trace_id=%s", trace_id)

    try:
        candidate = _get_candidate(trace_id)

        proposal = _build_proposal(
            candidate=candidate,
            trace_id=trace_id,
            compensation_ton=compensation_ton,
            termination_terms=termination_terms,
            justification=justification,
        )

        logger.info("Hire proposal compiled for %s (author=%s)",
                     trace_id, candidate.get("author"))
        return _wrap("ok", proposal)

    except ValueError as exc:
        logger.error("Candidate not found: %s", exc)
        return _wrap("error", {"error": str(exc)})
    except Exception as exc:
        logger.error("Hire proposal error: %s", exc, exc_info=True)
        return _wrap("error", {"error": str(exc)})
