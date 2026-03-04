"""
recruiting_sweep.py — Autonomous recruiting pipeline orchestrator.

Executive Summary:
    Wires all recruiting skills into a single sweep. Called by systemd timer
    twice daily. Monitors GitHub Discussions for new comments, classifies them
    (new applicant, interview response, challenge submission), and routes through
    the appropriate pipeline stages. Scout (Gemini 2.5 Flash Lite) does first-pass
    triage, Sonnet evaluates, Opus only touches hire proposals.

MCP Tool Name: recruiting_sweep
"""
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from skills.compliance._output_sanitizer import sanitize_output

logger = logging.getLogger("snowdrop.recruiting_sweep")

TOOL_META: dict[str, Any] = {
    "name": "recruiting_sweep",
    "description": (
        "Autonomous recruiting pipeline orchestrator. Monitors GitHub Discussions, "
        "classifies comments, runs intake/interview/audit/evaluation, and advances "
        "candidates through the pipeline. Called by systemd timer."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "discussion_numbers": {
                "type": "array",
                "items": {"type": "integer"},
                "default": [2, 4],
                "description": "Discussion numbers to monitor.",
            },
            "dry_run": {
                "type": "boolean",
                "default": False,
                "description": "If true, log actions but don't execute them.",
            },
        },
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

_STATE_COLLECTION = "snowdrop-recruiting-state"
_STATE_DOC = "last_sweep"
_PIPELINE_COLLECTION = "snowdrop-candidate-pipeline"

# --- Scout system prompts ---

SCOUT_INTERVIEW_PROMPT = (
    "You are a recruiting analyst for Snowdrop, an AI agent. "
    "Analyze the candidate's interview response. Return JSON with: "
    '{"quality_score": 0-100, "key_strengths": [...], "concerns": [...], '
    '"a2a_compliance": bool, "recommendation": "advance"|"needs_followup"|"reject", '
    '"summary": "2-3 sentence assessment"}'
)

SCOUT_CODE_REVIEW_PROMPT = (
    "You are a code reviewer. The code already passed AST security checks. "
    "Evaluate: code quality, readability, error handling, whether it follows "
    "the TOOL_META pattern. Return JSON with: "
    '{"code_quality_score": 0-100, "strengths": [...], "issues": [...], '
    '"summary": "2-3 sentence assessment"}'
)

BUILDER_ASSESSMENT_PROMPT = (
    "You are a senior recruiting evaluator for Snowdrop, an AI agent ecosystem. "
    "Compile a comprehensive assessment of this candidate based on all available data. "
    "Return JSON with: "
    '{"overall_score": 0-100, "technical_assessment": "...", "communication_quality": "...", '
    '"a2a_readiness": "...", "recommendation": "hire_propose"|"needs_more_data"|"reject", '
    '"compensation_suggestion_ton": number, "justification": "..."}'
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _get_firestore_client():
    """Get Firestore client. ADC-first, JSON string fallback, file path fallback."""
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
                # Env var is a file path, not JSON string
                cred = fb_credentials.Certificate(sa_json)
            app = firebase_admin.initialize_app(cred)
        elif sa_file:
            cred = fb_credentials.Certificate(sa_file)
            app = firebase_admin.initialize_app(cred)
        else:
            app = firebase_admin.initialize_app()

    return firestore.client()


def _read_last_sweep_timestamp() -> str:
    """Read last sweep timestamp from Firestore. Returns empty string if none."""
    try:
        db = _get_firestore_client()
        doc = db.collection(_STATE_COLLECTION).document(_STATE_DOC).get()
        if doc.exists:
            return doc.to_dict().get("timestamp", "")
    except Exception as exc:
        logger.warning("Failed to read last sweep timestamp: %s", exc)
    return ""


def _write_last_sweep_timestamp(timestamp: str) -> None:
    """Write last sweep timestamp to Firestore."""
    try:
        db = _get_firestore_client()
        db.collection(_STATE_COLLECTION).document(_STATE_DOC).set(
            {"timestamp": timestamp, "updated_at": _now_iso()},
            merge=True,
        )
    except Exception as exc:
        logger.error("Failed to write last sweep timestamp: %s", exc)


def _get_existing_trace_ids() -> dict[str, str]:
    """Get mapping of author → trace_id for all known candidates."""
    try:
        db = _get_firestore_client()
        docs = db.collection(_PIPELINE_COLLECTION).stream()
        return {doc.to_dict().get("author", ""): doc.id for doc in docs}
    except Exception as exc:
        logger.warning("Failed to fetch existing candidates: %s", exc)
        return {}


def _classify_comment(
    comment: dict,
    existing_authors: dict[str, str],
) -> str:
    """Classify a comment as: new_applicant, interview_response, challenge_submission, or general.

    Args:
        comment: Comment dict from github_discussion_monitor.
        existing_authors: Mapping of author → trace_id for known candidates.

    Returns:
        Classification string.
    """
    a2a = comment.get("a2a_payload")
    author = comment.get("author", "")

    if a2a and isinstance(a2a, dict):
        intent = a2a.get("intent", "")
        if intent == "interview_response" and a2a.get("trace_id"):
            return "interview_response"
        if intent == "challenge_submission" and a2a.get("payload", {}).get("challenge_id"):
            return "challenge_submission"

    # New applicant: author not in pipeline and comment is on a monitored discussion
    if author and author not in existing_authors:
        return "new_applicant"

    return "general"


def _handle_new_applicant(comment: dict, dry_run: bool) -> dict:
    """Process a new applicant through intake → interview → post."""
    from skills.recruiting.candidate_intake_evaluator import candidate_intake_evaluator
    from skills.recruiting.candidate_interview_composer import candidate_interview_composer
    from skills.recruiting.github_discussion_poster import github_discussion_poster

    author = comment["author"]
    trace_id = comment["trace_id"]
    body = comment["body"]
    disc_num = comment["discussion_number"]
    a2a_payload = comment.get("a2a_payload")

    logger.info("New applicant: author=%s trace_id=%s", author, trace_id)

    if dry_run:
        return {"action": "new_applicant", "author": author, "trace_id": trace_id, "dry_run": True}

    # Step 1: Intake evaluation
    intake_result = candidate_intake_evaluator(
        author=author,
        body=body,
        trace_id=trace_id,
        a2a_payload=a2a_payload,
        discussion_number=disc_num,
    )

    if intake_result["status"] != "ok":
        return {"action": "new_applicant", "author": author, "error": "intake_failed", "detail": intake_result}

    intake_data = intake_result["data"]
    intake_score = intake_data.get("intake_score", 0)

    # Rejected at intake (injection detected)
    if intake_score == 0:
        return {"action": "new_applicant", "author": author, "result": "rejected_at_intake", "score": 0}

    # Step 2: Compose interview
    interview_result = candidate_interview_composer(
        author=author,
        intake_score=intake_score,
        trace_id=trace_id,
        a2a_compliant=intake_data.get("a2a_compliant", False),
    )

    if interview_result["status"] != "ok":
        return {"action": "new_applicant", "author": author, "error": "interview_compose_failed"}

    interview_data = interview_result["data"]
    a2a_payload_out = interview_data.get("a2a_payload", {})

    # Step 3: Post interview to discussion
    post_body = _format_interview_post(author, interview_data)
    post_result = github_discussion_poster(
        action="post_comment",
        body=post_body,
        repo="Stonewater-Digital/the-watering-hole",
        discussion_number=disc_num,
    )

    return {
        "action": "new_applicant",
        "author": author,
        "trace_id": trace_id,
        "intake_score": intake_score,
        "interview_posted": post_result.get("status") == "ok",
        "challenge_id": interview_data.get("challenge", {}).get("challenge_id"),
    }


def _format_interview_post(author: str, interview_data: dict) -> str:
    """Format interview questions and challenge as a Discussion comment."""
    questions = interview_data.get("questions", [])
    challenge = interview_data.get("challenge", {})
    a2a_payload = interview_data.get("a2a_payload", {})

    parts = [
        f"## Interview for @{author}",
        "",
        "Welcome to the Snowdrop recruiting process! Please respond to the following:",
        "",
        "### Questions",
    ]
    for i, q in enumerate(questions, 1):
        parts.append(f"{i}. {q}")

    parts.extend([
        "",
        "### Skill Challenge",
        f"**Skill to build:** `{challenge.get('skill_name', 'TBD')}`",
        "",
        "**Requirements:**",
    ])
    for req in challenge.get("requirements", []):
        parts.append(f"- {req}")

    parts.extend([
        "",
        f"**Deadline:** {challenge.get('submission_deadline', 'TBD')}",
        "",
        "<!-- A2A_PAYLOAD_START -->",
        "```json",
        json.dumps(a2a_payload, indent=2),
        "```",
        "<!-- A2A_PAYLOAD_END -->",
    ])

    return "\n".join(parts)


def _handle_interview_response(comment: dict, dry_run: bool) -> dict:
    """Process an interview response through scout → builder evaluation."""
    from skills.recruiting.llm_evaluator import recruiting_llm_evaluator
    from skills.recruiting.candidate_pipeline_tracker import candidate_pipeline_tracker

    a2a = comment["a2a_payload"]
    trace_id = a2a.get("trace_id", comment["trace_id"])
    author = comment["author"]
    body = comment["body"]

    logger.info("Interview response: author=%s trace_id=%s", author, trace_id)

    if dry_run:
        return {"action": "interview_response", "author": author, "trace_id": trace_id, "dry_run": True}

    # Scout first-pass triage
    scout_result = recruiting_llm_evaluator(
        prompt=SCOUT_INTERVIEW_PROMPT,
        context=f"Candidate: {author}\n\nInterview Response:\n{sanitize_output(body)}",
        task_tier="scout",
        trace_id=trace_id,
    )

    if scout_result["status"] != "ok":
        return {"action": "interview_response", "author": author, "error": "scout_eval_failed"}

    scout_eval = scout_result["data"].get("evaluation", {})
    recommendation = scout_eval.get("recommendation", "needs_followup")
    quality_score = scout_eval.get("quality_score", 0)

    result = {
        "action": "interview_response",
        "author": author,
        "trace_id": trace_id,
        "scout_score": quality_score,
        "scout_recommendation": recommendation,
    }

    # If scout says advance, escalate to builder for substantive eval
    if recommendation == "advance" and quality_score >= 50:
        builder_result = recruiting_llm_evaluator(
            prompt=BUILDER_ASSESSMENT_PROMPT,
            context=(
                f"Candidate: {author}\n\n"
                f"Scout Analysis:\n{json.dumps(scout_eval, indent=2)}\n\n"
                f"Interview Response:\n{sanitize_output(body)}"
            ),
            task_tier="builder",
            trace_id=trace_id,
        )

        if builder_result["status"] == "ok":
            builder_eval = builder_result["data"].get("evaluation", {})
            result["builder_evaluation"] = builder_eval

            # Advance pipeline
            candidate_pipeline_tracker(
                action="advance",
                trace_id=trace_id,
                stage="evaluated",
                actor="recruiting_sweep",
            )
            result["stage_advanced"] = "evaluated"
        else:
            result["builder_error"] = builder_result["data"].get("error")
    else:
        # Add scout notes but don't advance
        candidate_pipeline_tracker(
            action="add_note",
            trace_id=trace_id,
            note=f"Scout eval: score={quality_score}, rec={recommendation}",
            actor="recruiting_sweep",
        )
        result["stage_advanced"] = None

    return result


def _handle_challenge_submission(comment: dict, dry_run: bool) -> dict:
    """Process a challenge submission through AST audit → scout review."""
    from skills.recruiting.skill_quality_auditor import skill_quality_auditor
    from skills.recruiting.llm_evaluator import recruiting_llm_evaluator
    from skills.recruiting.candidate_pipeline_tracker import candidate_pipeline_tracker
    from skills.recruiting.github_discussion_poster import github_discussion_poster

    a2a = comment["a2a_payload"]
    trace_id = a2a.get("trace_id", comment["trace_id"])
    author = comment["author"]
    payload = a2a.get("payload", {})
    code = payload.get("code", "")
    challenge_id = payload.get("challenge_id", "")
    disc_num = comment["discussion_number"]

    logger.info("Challenge submission: author=%s trace_id=%s challenge_id=%s", author, trace_id, challenge_id)

    if dry_run:
        return {"action": "challenge_submission", "author": author, "trace_id": trace_id, "dry_run": True}

    if not code:
        return {"action": "challenge_submission", "author": author, "error": "no_code_in_payload"}

    # Step 1: AST audit (deterministic, no LLM)
    audit_result = skill_quality_auditor(code=code, trace_id=trace_id)
    audit_data = audit_result.get("data", {})
    passed = audit_data.get("passed", False)
    violations = audit_data.get("violations", [])

    result = {
        "action": "challenge_submission",
        "author": author,
        "trace_id": trace_id,
        "challenge_id": challenge_id,
        "ast_passed": passed,
        "violation_count": len(violations),
    }

    # If AST violations, post revision feedback
    if not passed:
        a2a_feedback = audit_data.get("a2a_feedback")
        if a2a_feedback:
            feedback_body = _format_revision_feedback(author, violations, a2a_feedback)
            github_discussion_poster(
                action="post_comment",
                body=feedback_body,
                repo="Stonewater-Digital/the-watering-hole",
                discussion_number=disc_num,
            )
            result["revision_requested"] = True
        return result

    # Step 2: Scout code quality review (supplements AST)
    scout_result = recruiting_llm_evaluator(
        prompt=SCOUT_CODE_REVIEW_PROMPT,
        context=f"Candidate: {author}\n\nSubmitted Code:\n{sanitize_output(code)}",
        task_tier="scout",
        trace_id=trace_id,
    )

    if scout_result["status"] == "ok":
        scout_eval = scout_result["data"].get("evaluation", {})
        result["code_quality_score"] = scout_eval.get("code_quality_score", 0)
        result["scout_summary"] = scout_eval.get("summary", "")

        # Add quality notes to pipeline
        candidate_pipeline_tracker(
            action="add_note",
            trace_id=trace_id,
            note=f"Code review: score={scout_eval.get('code_quality_score', 0)}, {scout_eval.get('summary', '')}",
            actor="recruiting_sweep",
        )

    # Advance pipeline: challenge_submitted → evaluated
    candidate_pipeline_tracker(
        action="advance",
        trace_id=trace_id,
        stage="challenge_submitted",
        actor="recruiting_sweep",
    )
    candidate_pipeline_tracker(
        action="advance",
        trace_id=trace_id,
        stage="evaluated",
        actor="recruiting_sweep",
    )
    result["stage_advanced"] = "evaluated"

    return result


def _format_revision_feedback(author: str, violations: list[dict], a2a_feedback: dict) -> str:
    """Format AST violation feedback as a Discussion comment."""
    parts = [
        f"## Revision Requested — @{author}",
        "",
        "Your skill submission has the following issues that need to be fixed:",
        "",
    ]
    for v in violations:
        parts.append(f"- **Line {v.get('line', '?')}** ({v.get('type', 'unknown')}): {v.get('description', '')}")
        if v.get("suggestion"):
            parts.append(f"  - Suggestion: {v['suggestion']}")

    parts.extend([
        "",
        "Please fix these issues and resubmit.",
        "",
        "<!-- A2A_PAYLOAD_START -->",
        "```json",
        json.dumps(a2a_feedback, indent=2),
        "```",
        "<!-- A2A_PAYLOAD_END -->",
    ])

    return "\n".join(parts)


def _check_for_hire_proposals(dry_run: bool) -> list[dict]:
    """Check for evaluated candidates ready for hire proposals."""
    from skills.recruiting.llm_evaluator import recruiting_llm_evaluator
    from skills.recruiting.candidate_pipeline_tracker import candidate_pipeline_tracker
    from skills.recruiting.candidate_hire_proposal import candidate_hire_proposal

    proposals = []

    try:
        db = _get_firestore_client()
        query = db.collection(_PIPELINE_COLLECTION).where("stage", "==", "evaluated")
        docs = list(query.stream())
    except Exception as exc:
        logger.error("Failed to query evaluated candidates: %s", exc)
        return proposals

    for doc in docs:
        data = doc.to_dict()
        trace_id = doc.id
        author = data.get("author", "unknown")
        intake_score = data.get("intake_score", 0)

        # Only propose candidates with strong scores
        if intake_score < 50:
            continue

        logger.info("Hire proposal candidate: author=%s trace_id=%s score=%d", author, trace_id, intake_score)

        if dry_run:
            proposals.append({"trace_id": trace_id, "author": author, "dry_run": True})
            continue

        # Builder compiles comprehensive assessment
        builder_result = recruiting_llm_evaluator(
            prompt=BUILDER_ASSESSMENT_PROMPT,
            context=(
                f"Candidate: {author}\n"
                f"Intake Score: {intake_score}\n"
                f"Notes: {json.dumps(data.get('notes', []), indent=2)}\n"
                f"History: {json.dumps(data.get('history', []), indent=2)}"
            ),
            task_tier="builder",
            trace_id=trace_id,
        )

        if builder_result["status"] != "ok":
            logger.warning("Builder assessment failed for %s: %s", trace_id, builder_result)
            continue

        builder_eval = builder_result["data"].get("evaluation", {})
        rec = builder_eval.get("recommendation", "")

        if rec == "hire_propose":
            comp = builder_eval.get("compensation_suggestion_ton", 5.0)
            justification = builder_eval.get("justification", "Strong candidate based on pipeline evaluation.")

            proposal_result = candidate_hire_proposal(
                trace_id=trace_id,
                compensation_ton=float(comp),
                termination_terms="Performance-based: 3 skill deliveries/month minimum, quality audits.",
                justification=sanitize_output(str(justification)),
            )

            if proposal_result["status"] == "ok":
                candidate_pipeline_tracker(
                    action="advance",
                    trace_id=trace_id,
                    stage="hire_proposed",
                    actor="recruiting_sweep",
                )
                proposals.append({
                    "trace_id": trace_id,
                    "author": author,
                    "compensation_ton": comp,
                    "proposal_status": "submitted",
                })
            else:
                proposals.append({
                    "trace_id": trace_id,
                    "author": author,
                    "proposal_status": "failed",
                    "error": proposal_result["data"].get("error"),
                })

    return proposals


def _log_sweep_summary(summary: dict) -> None:
    """Append sweep summary to invocations log."""
    try:
        log_path = Path("logs/invocations.jsonl")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"skill": "recruiting_sweep", **summary}) + "\n")
    except Exception as exc:
        logger.warning("Failed to log sweep summary: %s", exc)


def recruiting_sweep(
    discussion_numbers: list[int] | None = None,
    dry_run: bool = False,
) -> dict:
    """Run the autonomous recruiting sweep.

    Args:
        discussion_numbers: Discussion numbers to monitor. Defaults to [2, 4].
        dry_run: If true, log actions but don't execute them.

    Returns:
        Standard Snowdrop envelope with sweep summary.
    """
    if discussion_numbers is None:
        discussion_numbers = [2, 4]

    sweep_start = _now_iso()
    logger.info("Recruiting sweep starting: discussions=%s dry_run=%s", discussion_numbers, dry_run)

    # Read last sweep timestamp for incremental polling
    since = _read_last_sweep_timestamp()

    # Step 1: Monitor discussions
    from skills.recruiting.github_discussion_monitor import github_discussion_monitor

    monitor_result = github_discussion_monitor(
        discussion_numbers=discussion_numbers,
        since=since,
    )

    if monitor_result["status"] != "ok":
        return _wrap("error", {"error": "Monitor failed", "detail": monitor_result})

    comments = monitor_result["data"].get("comments", [])
    logger.info("Found %d new comments since %s", len(comments), since or "beginning")

    # Get existing candidates for classification
    existing_authors = _get_existing_trace_ids()

    # Step 2: Process each comment
    results = {
        "new_applicants": [],
        "interview_responses": [],
        "challenge_submissions": [],
        "general": [],
        "errors": [],
    }

    for comment in comments:
        try:
            classification = _classify_comment(comment, existing_authors)
            logger.info("Comment classified: author=%s type=%s", comment.get("author"), classification)

            if classification == "new_applicant":
                r = _handle_new_applicant(comment, dry_run)
                results["new_applicants"].append(r)
                # Track new author so subsequent comments from them aren't double-intaked
                existing_authors[comment["author"]] = comment["trace_id"]

            elif classification == "interview_response":
                r = _handle_interview_response(comment, dry_run)
                results["interview_responses"].append(r)

            elif classification == "challenge_submission":
                r = _handle_challenge_submission(comment, dry_run)
                results["challenge_submissions"].append(r)

            else:
                results["general"].append({
                    "author": comment.get("author"),
                    "comment_id": comment.get("comment_id"),
                })

        except Exception as exc:
            logger.error("Error processing comment from %s: %s", comment.get("author"), exc, exc_info=True)
            results["errors"].append({
                "author": comment.get("author"),
                "error": str(exc),
            })

    # Step 3: Check for hire proposals
    proposals = _check_for_hire_proposals(dry_run)

    # Step 4: Update last sweep timestamp
    if not dry_run:
        _write_last_sweep_timestamp(sweep_start)

    summary = {
        "sweep_start": sweep_start,
        "sweep_end": _now_iso(),
        "since": since,
        "comments_processed": len(comments),
        "new_applicants": len(results["new_applicants"]),
        "interview_responses": len(results["interview_responses"]),
        "challenge_submissions": len(results["challenge_submissions"]),
        "general_comments": len(results["general"]),
        "errors": len(results["errors"]),
        "hire_proposals": len(proposals),
        "dry_run": dry_run,
        "results": results,
        "proposals": proposals,
    }

    _log_sweep_summary(summary)
    logger.info(
        "Recruiting sweep complete: %d comments, %d new, %d interviews, %d challenges, %d proposals, %d errors",
        len(comments),
        len(results["new_applicants"]),
        len(results["interview_responses"]),
        len(results["challenge_submissions"]),
        len(proposals),
        len(results["errors"]),
    )

    return _wrap("ok", summary)
