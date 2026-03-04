"""
Executive Summary
-----------------
Lists Firebase AI Logic (formerly Vertex AI in Firebase) server-side prompt templates
for a GCP project. Tries the Firebase-specific endpoint first and falls back to the
Vertex AI cachedContents endpoint gracefully. Returns template metadata including
model configuration and system instruction previews.

Credentials resolved ADC-first (Cloud Run), then GOOGLE_SERVICE_ACCOUNT_JSON (local dev).

Inputs:
  project_id : str | None — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  location   : str        — GCP region, default "us-central1"
  page_size  : int        — maximum number of templates to return, default 20

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_ai_logic_list_prompts

Agent Notes:
  - Required IAM: roles/aiplatform.user or roles/firebase.viewer
  - The Firebase AI Logic prompt template API is currently in preview; availability
    may vary by region.
  - Falls back to Vertex AI cachedContents if the Firebase-specific endpoint returns
    a 404 or 403.
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_ai_logic_list_prompts")

TOOL_META = {
    "name": "firebase_ai_logic_list_prompts",
    "description": (
        "List Firebase AI Logic server-side prompt templates for a project. "
        "Returns template IDs, model configurations, and system instructions."
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


def _parse_template(raw: dict) -> dict:
    """Normalize a raw Firebase or Vertex API template record into a flat summary.

    Args:
        raw: Raw dict from either the Firebase AI Logic or Vertex cachedContents API.

    Returns:
        Normalized dict with consistent keys.
    """
    name: str = raw.get("name", "")
    template_id: str = name.split("/")[-1] if name else raw.get("name", "")

    # Firebase AI Logic shape
    display_name: str = raw.get("displayName", "")
    model: str = raw.get("model", raw.get("model", ""))

    # System instruction may be in Firebase or Vertex format
    system_instruction_raw = raw.get("systemInstruction", raw.get("system_instruction", {}))
    if isinstance(system_instruction_raw, dict):
        parts = system_instruction_raw.get("parts", [])
        si_text = " ".join(
            p.get("text", "") for p in parts if isinstance(p, dict)
        ) if parts else ""
    elif isinstance(system_instruction_raw, str):
        si_text = system_instruction_raw
    else:
        si_text = ""

    # Truncate preview to 200 chars
    si_preview: str = si_text[:200] + ("..." if len(si_text) > 200 else "")

    return {
        "template_id": template_id,
        "display_name": display_name,
        "model": model,
        "system_instruction_preview": si_preview,
        "create_time": raw.get("createTime", raw.get("create_time", "")),
        "update_time": raw.get("updateTime", raw.get("update_time", "")),
    }


def firebase_ai_logic_list_prompts(
    project_id: str | None = None,
    location: str = "us-central1",
    page_size: int = 20,
) -> dict:
    """List Firebase AI Logic server-side prompt templates for a GCP project.

    Attempts the Firebase-specific promptTemplates endpoint first. Falls back to
    the Vertex AI cachedContents endpoint if the Firebase endpoint is unavailable
    (404 or 403). Both endpoints are authenticated with the same Cloud Platform
    OAuth2 token.

    Args:
        project_id: GCP project ID. Defaults to the ``GOOGLE_PROJECT_ID``
            environment variable when not provided.
        location: GCP region where Firebase AI Logic resources are hosted.
            Defaults to ``"us-central1"``.
        page_size: Maximum number of template records to return. Defaults to 20.

    Returns:
        dict with keys:
            - status (str): ``"ok"`` or ``"error"``.
            - data (dict): Contains ``templates`` (list), ``count`` (int),
              ``source`` (str indicating which endpoint responded), and
              ``location`` (str).
            - timestamp (str): ISO 8601 UTC execution timestamp.

    Raises:
        Does not raise; all exceptions are caught and returned as error dicts.

    Example:
        >>> result = firebase_ai_logic_list_prompts(project_id="my-gcp-project")
        >>> result["status"]
        'ok'
        >>> isinstance(result["data"]["templates"], list)
        True
    """
    logger.info(
        "firebase_ai_logic_list_prompts: entry project=%s location=%s page_size=%d",
        project_id,
        location,
        page_size,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        logger.error("firebase_ai_logic_list_prompts: project_id missing")
        return {
            "status": "error",
            "data": {"message": "project_id is required or set GOOGLE_PROJECT_ID"},
            "timestamp": _now(),
        }

    try:
        token = _get_access_token([_CLOUD_PLATFORM_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # --- Attempt 1: Firebase AI Logic endpoint ---
        firebase_url = (
            f"https://firebasevertexai.googleapis.com/v1/projects/{project_id}"
            f"/locations/{location}/promptTemplates"
        )
        params: dict = {"pageSize": page_size}

        logger.info("firebase_ai_logic_list_prompts: trying Firebase endpoint %s", firebase_url)
        fb_resp = requests.get(firebase_url, headers=headers, params=params, timeout=15)

        source: str
        templates: list[dict]

        if fb_resp.status_code == 200:
            body = fb_resp.json()
            raw_templates = body.get("promptTemplates", body.get("templates", []))
            templates = [_parse_template(t) for t in raw_templates]
            source = "firebase_ai_logic"
            logger.info(
                "firebase_ai_logic_list_prompts: Firebase endpoint returned %d templates",
                len(templates),
            )
        else:
            logger.warning(
                "firebase_ai_logic_list_prompts: Firebase endpoint returned %d — falling back to Vertex AI",
                fb_resp.status_code,
            )

            # --- Attempt 2: Vertex AI cachedContents fallback ---
            vertex_url = (
                f"https://{location}-aiplatform.googleapis.com/v1"
                f"/projects/{project_id}/locations/{location}/cachedContents"
            )
            logger.info(
                "firebase_ai_logic_list_prompts: trying Vertex fallback %s", vertex_url
            )
            vx_resp = requests.get(vertex_url, headers=headers, params=params, timeout=15)

            if vx_resp.status_code != 200:
                logger.error(
                    "firebase_ai_logic_list_prompts: Vertex fallback also failed: %d %s",
                    vx_resp.status_code,
                    vx_resp.text[:300],
                )
                return {
                    "status": "error",
                    "data": {
                        "message": (
                            f"Firebase endpoint: {fb_resp.status_code}; "
                            f"Vertex fallback: {vx_resp.status_code}"
                        ),
                        "firebase_response": fb_resp.text[:300],
                        "vertex_response": vx_resp.text[:300],
                    },
                    "timestamp": _now(),
                }

            body = vx_resp.json()
            raw_templates = body.get("cachedContents", [])
            templates = [_parse_template(t) for t in raw_templates]
            source = "vertex_ai_cached_contents"
            logger.info(
                "firebase_ai_logic_list_prompts: Vertex fallback returned %d records",
                len(templates),
            )

        logger.info(
            "firebase_ai_logic_list_prompts: exit success count=%d source=%s",
            len(templates),
            source,
        )
        return {
            "status": "ok",
            "data": {
                "templates": templates,
                "count": len(templates),
                "source": source,
                "location": location,
                "project_id": project_id,
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_ai_logic_list_prompts: unexpected error: %s", exc, exc_info=True)
        return {
            "status": "error",
            "data": {"message": str(exc)},
            "timestamp": _now(),
        }
