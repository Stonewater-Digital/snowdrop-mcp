"""
Executive Summary
-----------------
Lists ML models hosted in Firebase ML for a GCP project using the firebase-admin
SDK. Returns model ID, display name, creation time, last update time, tags, and
TFLite model download URI and size. Credentials are resolved via ADC on Cloud Run
or via GOOGLE_SERVICE_ACCOUNT_JSON for local and Railway deployments.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string (Cloud Run / Railway / Fly.io)
  2. ADC (Application Default Credentials) — used automatically on Cloud Run

Inputs:
  project_id : str       — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  page_size  : int       — max models to return (default 20)
  filter     : str|None  — optional filter string (e.g. "tags:myTag")

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_ml_list_models

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required: firebase-admin Python SDK installed in environment
  - Required IAM role: roles/firebaseml.viewer or roles/firebase.viewer
  - Models with no TFLite file will have tflite_model set to null
  - filter syntax: "tags:production" or "displayName:my-model*"
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials as fb_credentials

logger = logging.getLogger("snowdrop.firebase_ml_list_models")

TOOL_META = {
    "name": "firebase_ml_list_models",
    "description": (
        "List ML models hosted in Firebase ML for a project. "
        "Returns model ID, display name, creation time, and download URI."
    ),
    "tier": "free",
}

_fb_app: firebase_admin.App | None = None


def _get_fb_app() -> firebase_admin.App:
    """Initialize and cache the Firebase Admin app (singleton)."""
    global _fb_app
    if _fb_app is not None:
        return _fb_app
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        cred = fb_credentials.Certificate(json.loads(sa_json))
        _fb_app = firebase_admin.initialize_app(cred)
    else:
        _fb_app = firebase_admin.initialize_app()
    return _fb_app


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now()}


def _model_to_dict(model: object) -> dict:
    """Convert a firebase_admin.ml.Model object to a serialisable dict."""
    tflite_info = None
    try:
        tflite = getattr(model, "model_format", None)
        if tflite is not None:
            tflite_info = {
                "uri": getattr(tflite, "model_source", None),
                "size_bytes": getattr(tflite, "size_bytes", None),
            }
        else:
            # Try accessing as attribute directly for older SDK versions.
            tflite_model = getattr(model, "tflite_model", None)
            if tflite_model is not None:
                tflite_info = {
                    "uri": getattr(tflite_model, "gcs_tflite_uri", None),
                    "size_bytes": getattr(tflite_model, "size_bytes", None),
                }
    except Exception:
        pass

    return {
        "model_id": getattr(model, "model_id", ""),
        "display_name": getattr(model, "display_name", ""),
        "create_time": str(getattr(model, "create_time", "") or ""),
        "update_time": str(getattr(model, "update_time", "") or ""),
        "tags": list(getattr(model, "tags", []) or []),
        "tflite_model": tflite_info,
    }


def firebase_ml_list_models(
    project_id: str | None = None,
    page_size: int = 20,
    filter: str | None = None,
) -> dict:
    """List ML models hosted in Firebase ML for a project.

    Args:
        project_id: GCP project ID. Falls back to GOOGLE_PROJECT_ID env var
            if not supplied. Note: project_id is used to configure the Firebase
            Admin app; the SDK handles scoping automatically.
        page_size: Maximum number of models to return. Defaults to 20.
        filter: Optional filter string for narrowing results. Supports syntax
            such as "tags:myTag" or "displayName:my-model*". Defaults to None
            (return all models up to page_size).

    Returns:
        dict: Standard Snowdrop envelope::

            {
                "status": "ok",
                "data": {
                    "models": [
                        {
                            "model_id": str,
                            "display_name": str,
                            "create_time": str,
                            "update_time": str,
                            "tags": list[str],
                            "tflite_model": {
                                "uri": str,
                                "size_bytes": int
                            } | None
                        },
                        ...
                    ],
                    "count": int,
                    "project_id": str
                },
                "timestamp": "<ISO8601>"
            }

    Raises:
        RuntimeError: If no GCP credentials are available.

    Example:
        >>> result = firebase_ml_list_models(
        ...     project_id="my-firebase-project",
        ...     page_size=5,
        ...     filter="tags:production",
        ... )
        >>> print(result["data"]["count"])
        2
    """
    logger.info(
        "firebase_ml_list_models called: project_id=%s, page_size=%d, filter=%s",
        project_id,
        page_size,
        filter,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")

    try:
        _get_fb_app()
        from firebase_admin import ml

        page_size = min(max(1, page_size), 100)

        models_page = ml.list_models(list_filter=filter, page_size=page_size)

        # list_models returns a ListModelsPage; iterate to collect models.
        model_list = []
        for model in models_page.iterate_all():
            model_list.append(_model_to_dict(model))
            if len(model_list) >= page_size:
                break

        logger.info(
            "firebase_ml_list_models returned %d models for project %s",
            len(model_list),
            project_id,
        )
        return _wrap(
            "ok",
            {
                "models": model_list,
                "count": len(model_list),
                "project_id": project_id or "(from credentials)",
            },
        )

    except Exception as exc:
        logger.exception("Unexpected error in firebase_ml_list_models")
        return _wrap("error", {"message": str(exc)})
