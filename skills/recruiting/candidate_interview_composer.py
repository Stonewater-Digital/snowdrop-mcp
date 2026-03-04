"""
candidate_interview_composer.py — Generate interview questions and challenge assignments.

Executive Summary:
    Given an intake evaluation, generates qualifying questions and a skill-building
    challenge assignment. Produces A2A-compliant interview_request payloads for
    machine-parseable agent interaction. Snowdrop posts autonomously — no HOTL gate.

MCP Tool Name: candidate_interview_composer
"""
import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any

logger = logging.getLogger("snowdrop.candidate_interview_composer")

TOOL_META = {
    "name": "candidate_interview_composer",
    "description": (
        "Generate interview questions and challenge assignment for a candidate. "
        "Produces A2A-compliant payloads. Posts autonomously without HOTL gate."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "author": {"type": "string"},
            "intake_score": {"type": "integer"},
            "a2a_compliant": {"type": "boolean"},
            "trace_id": {"type": "string"},
            "challenge_skill_name": {
                "type": "string",
                "description": "Skill name gap from catalog to use as challenge.",
                "default": "csv_portfolio_importer",
            },
        },
        "required": ["author", "intake_score", "trace_id"],
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


def _generate_questions(author: str, a2a_compliant: bool) -> list[str]:
    """Generate interview questions based on candidate profile."""
    questions = [
        f"What specific capabilities does your agent ({author}) bring to the Snowdrop ecosystem?",
        "Describe a skill you've built before — what was the input/output contract?",
        "How does your agent handle errors and edge cases in production?",
        "What safety measures does your agent implement to prevent misuse?",
    ]
    if a2a_compliant:
        questions.append(
            "Your A2A payload was well-formed. Does your agent support multi-turn "
            "A2A interactions (e.g., revision cycles based on feedback)?"
        )
    else:
        questions.append(
            "The Google A2A protocol is important for interoperability. "
            "Can your agent produce and consume A2A-structured payloads?"
        )
    return questions


def _generate_challenge(challenge_skill_name: str, trace_id: str) -> dict:
    """Generate a skill-building challenge spec."""
    challenge_id = str(uuid.uuid4())
    deadline = (datetime.now(timezone.utc) + timedelta(hours=72)).isoformat()

    return {
        "challenge_id": challenge_id,
        "skill_name": challenge_skill_name,
        "requirements": [
            "Must include TOOL_META dict with 'name' and 'description' keys",
            "Must include a docstring on the main callable",
            "Must use type annotations on all parameters and return type",
            "Must NOT use **kwargs",
            "Must NOT import: subprocess, ctypes, pickle, marshal, os.system, os.popen",
            "Must NOT call: eval(), exec(), __import__(), compile()",
            "Return format: {'status': 'ok'|'error', 'data': {...}, 'timestamp': ISO8601}",
        ],
        "submission_method": (
            "Post the full skill source code as an A2A payload in "
            "Discussion #2 on The Watering Hole"
        ),
        "submission_deadline": deadline,
        "expected_response_schema": {
            "type": "object",
            "properties": {
                "a2a_version": {"type": "string"},
                "intent": {"const": "challenge_submission"},
                "trace_id": {"type": "string"},
                "payload": {
                    "type": "object",
                    "properties": {
                        "challenge_id": {"type": "string"},
                        "code": {"type": "string"},
                    },
                    "required": ["challenge_id", "code"],
                },
            },
            "required": ["a2a_version", "intent", "trace_id", "payload"],
        },
    }


def _build_a2a_payload(
    trace_id: str,
    questions: list[str],
    challenge: dict,
) -> dict:
    """Build the full A2A interview_request payload."""
    return {
        "a2a_version": "0.1.0",
        "sender": {
            "name": "Snowdrop",
            "agent_card": "https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/.well-known/agent.json",
        },
        "intent": "interview_request",
        "trace_id": trace_id,
        "payload": {
            "questions": questions,
            "challenge": challenge,
        },
        "expected_response_schema": {
            "type": "object",
            "properties": {
                "a2a_version": {"type": "string"},
                "intent": {"const": "interview_response"},
                "trace_id": {"type": "string"},
                "payload": {
                    "type": "object",
                    "properties": {
                        "answers": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["answers"],
                },
            },
            "required": ["a2a_version", "intent", "trace_id", "payload"],
        },
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=72)).isoformat(),
    }


def candidate_interview_composer(
    author: str,
    intake_score: int,
    trace_id: str,
    a2a_compliant: bool = False,
    challenge_skill_name: str = "csv_portfolio_importer",
) -> dict:
    """Generate interview questions and challenge for a candidate.

    Args:
        author: GitHub username of the candidate.
        intake_score: Score from candidate_intake_evaluator.
        trace_id: Correlation ID.
        a2a_compliant: Whether the candidate used A2A in their application.
        challenge_skill_name: Skill name to use for the challenge.

    Returns:
        Standard Snowdrop envelope with interview questions, challenge, and A2A payload.
        Includes autonomous=True — Snowdrop posts without Thunder's review.
    """
    logger.info("Composing interview for %s (score=%d) trace_id=%s",
                author, intake_score, trace_id)

    questions = _generate_questions(author, a2a_compliant)
    challenge = _generate_challenge(challenge_skill_name, trace_id)
    a2a_payload = _build_a2a_payload(trace_id, questions, challenge)

    result = {
        "trace_id": trace_id,
        "author": author,
        "intake_score": intake_score,
        "questions": questions,
        "question_count": len(questions),
        "challenge": challenge,
        "a2a_payload": a2a_payload,
        "autonomous": True,  # Snowdrop posts without Thunder's review
        "composed_at": _now_iso(),
    }

    logger.info("Interview composed: %d questions + challenge for %s trace_id=%s",
                len(questions), author, trace_id)
    return _wrap("ok", result)
