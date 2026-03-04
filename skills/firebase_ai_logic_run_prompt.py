"""
Executive Summary
-----------------
Executes a generative AI request against Google's Vertex AI generateContent endpoint,
optionally using a Firebase AI Logic prompt template ID as a reference identifier.
Accepts a user message and optional system instruction directly, or a template_id
with variables for future template resolution. Returns the model's text response,
finish reason, and token usage metadata.

Credentials resolved ADC-first (Cloud Run), then GOOGLE_SERVICE_ACCOUNT_JSON (local dev).

Inputs:
  user_message       : str            — user turn content (required)
  system_instruction : str | None     — system-level prompt override
  template_id        : str | None     — Firebase AI Logic template identifier (for logging/routing)
  variables          : dict | None    — substitution variables for template (for future use)
  project_id         : str | None     — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  location           : str            — GCP region, default "us-central1"
  model              : str            — Vertex AI model ID, default "gemini-2.0-flash-001"

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_ai_logic_run_prompt

Agent Notes:
  - Required IAM: roles/aiplatform.user
  - The model field accepts any publisher model available in the specified region.
  - Token counts come from usageMetadata in the Vertex API response.
  - variables dict is available for future template resolution; currently logged only.
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

from config.models import resolve_model

logger = logging.getLogger("snowdrop.firebase_ai_logic_run_prompt")

TOOL_META = {
    "name": "firebase_ai_logic_run_prompt",
    "description": (
        "Execute a Firebase AI Logic prompt template with provided variables. "
        "Returns the model's text response."
    ),
    "tier": "free",
}

_CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


def _get_access_token(scopes: list[str]) -> str:
    """Get an OAuth2 access token. ADC-first (Cloud Run), JSON fallback (local dev).

    Args:
        scopes: List of OAuth2 scope strings to request.

    Returns:
        A valid Bearer token string.

    Raises:
        RuntimeError: If no credential source is available.
    """
    import google.auth.transport.requests

    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json), scopes=scopes
        )
    else:
        import google.auth
        creds, _ = google.auth.default(scopes=scopes)
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


def _now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _apply_variables(text: str, variables: dict) -> str:
    """Substitute ``{key}`` placeholders in text with values from variables dict.

    Args:
        text: Template string containing ``{key}`` placeholders.
        variables: Mapping of placeholder names to replacement values.

    Returns:
        String with all matching placeholders replaced.
    """
    for key, value in variables.items():
        text = text.replace(f"{{{key}}}", str(value))
    return text


def firebase_ai_logic_run_prompt(
    user_message: str,
    system_instruction: str | None = None,
    template_id: str | None = None,
    variables: dict | None = None,
    project_id: str | None = None,
    location: str = "us-central1",
    model: str | None = None,
) -> dict:
    """Execute a generative AI request via the Vertex AI generateContent endpoint.

    Builds a Vertex AI ``generateContent`` request from the provided user message
    and optional system instruction. If ``template_id`` is provided it is included
    in the response metadata for traceability. If ``variables`` are provided they
    are substituted into both the system instruction and user message using
    ``{key}`` syntax before the API call is made.

    Args:
        user_message: The user-turn text to send to the model. Required.
        system_instruction: Optional system-level instruction prepended to the
            conversation. Supports ``{key}`` variable substitution.
        template_id: Optional Firebase AI Logic template identifier. Used for
            logging and response metadata; template resolution is not yet
            implemented server-side.
        variables: Optional dict of ``{key: value}`` substitutions applied to
            both ``system_instruction`` and ``user_message`` before the API call.
        project_id: GCP project ID. Defaults to the ``GOOGLE_PROJECT_ID``
            environment variable when not provided.
        location: GCP region hosting the model endpoint. Defaults to
            ``"us-central1"``.
        model: Vertex AI publisher model ID. Defaults to
            ``"gemini-2.0-flash-001"``.

    Returns:
        dict with keys:
            - status (str): ``"ok"`` or ``"error"``.
            - data (dict): Contains ``response_text`` (str), ``finish_reason`` (str),
              ``usage_metadata`` (dict with ``input_tokens`` and ``output_tokens``),
              ``model`` (str), ``template_id`` (str | None), and ``location`` (str).
            - timestamp (str): ISO 8601 UTC execution timestamp.

    Raises:
        Does not raise; all exceptions are caught and returned as error dicts.

    Example:
        >>> result = firebase_ai_logic_run_prompt(
        ...     user_message="Summarize the Q3 earnings in one sentence.",
        ...     system_instruction="You are a concise financial analyst.",
        ...     project_id="my-gcp-project",
        ... )
        >>> result["status"]
        'ok'
        >>> isinstance(result["data"]["response_text"], str)
        True
    """
    if model is None:
        _secretary = resolve_model("secretary")
        # resolve_model returns "provider/model_id"; Vertex needs bare model_id
        model = _secretary.split("/", 1)[-1]

    logger.info(
        "firebase_ai_logic_run_prompt: entry template_id=%s model=%s location=%s",
        template_id,
        model,
        location,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        logger.error("firebase_ai_logic_run_prompt: project_id missing")
        return {
            "status": "error",
            "data": {"message": "project_id is required or set GOOGLE_PROJECT_ID"},
            "timestamp": _now(),
        }

    if not user_message or not user_message.strip():
        logger.error("firebase_ai_logic_run_prompt: user_message is empty")
        return {
            "status": "error",
            "data": {"message": "user_message must not be empty"},
            "timestamp": _now(),
        }

    try:
        vars_map: dict = variables or {}

        # Apply variable substitution
        resolved_user_message = _apply_variables(user_message, vars_map)
        resolved_system: str | None = (
            _apply_variables(system_instruction, vars_map)
            if system_instruction
            else None
        )

        if vars_map:
            logger.info(
                "firebase_ai_logic_run_prompt: applied %d variable(s)", len(vars_map)
            )

        # Build request body
        request_body: dict = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": resolved_user_message}],
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
            },
        }

        if resolved_system:
            request_body["systemInstruction"] = {
                "parts": [{"text": resolved_system}]
            }

        token = _get_access_token([_CLOUD_PLATFORM_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = (
            f"https://{location}-aiplatform.googleapis.com/v1"
            f"/projects/{project_id}/locations/{location}"
            f"/publishers/google/models/{model}:generateContent"
        )

        logger.info("firebase_ai_logic_run_prompt: POST %s", url)
        resp = requests.post(url, headers=headers, json=request_body, timeout=60)

        if resp.status_code != 200:
            logger.error(
                "firebase_ai_logic_run_prompt: API error %d: %s",
                resp.status_code,
                resp.text[:400],
            )
            return {
                "status": "error",
                "data": {
                    "message": f"Vertex API returned {resp.status_code}",
                    "detail": resp.text[:400],
                },
                "timestamp": _now(),
            }

        body = resp.json()

        # Extract response text from candidates
        candidates = body.get("candidates", [])
        response_text = ""
        finish_reason = ""
        if candidates:
            first = candidates[0]
            finish_reason = first.get("finishReason", "")
            content = first.get("content", {})
            parts = content.get("parts", [])
            response_text = "".join(
                p.get("text", "") for p in parts if isinstance(p, dict)
            )

        # Extract token usage
        usage_meta = body.get("usageMetadata", {})
        usage_metadata = {
            "input_tokens": usage_meta.get("promptTokenCount", 0),
            "output_tokens": usage_meta.get("candidatesTokenCount", 0),
            "total_tokens": usage_meta.get("totalTokenCount", 0),
        }

        logger.info(
            "firebase_ai_logic_run_prompt: exit success finish_reason=%s tokens_in=%d tokens_out=%d",
            finish_reason,
            usage_metadata["input_tokens"],
            usage_metadata["output_tokens"],
        )

        return {
            "status": "ok",
            "data": {
                "response_text": response_text,
                "finish_reason": finish_reason,
                "usage_metadata": usage_metadata,
                "model": model,
                "template_id": template_id,
                "location": location,
                "project_id": project_id,
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error(
            "firebase_ai_logic_run_prompt: unexpected error: %s", exc, exc_info=True
        )
        return {
            "status": "error",
            "data": {"message": str(exc)},
            "timestamp": _now(),
        }
