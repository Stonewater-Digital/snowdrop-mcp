"""
Executive Summary
-----------------
Retrieves detailed information about a specific Firebase ML model using the
firebase-admin SDK, including its TFLite download URI, file size, and SHA-256
hash for integrity verification. Also surfaces any validation errors reported by
Firebase ML. Credentials are resolved via ADC on Cloud Run or via
GOOGLE_SERVICE_ACCOUNT_JSON for local and Railway deployments.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — raw JSON string (Cloud Run / Railway / Fly.io)
  2. ADC (Application Default Credentials) — used automatically on Cloud Run

Inputs:
  model_id   : str  — Firebase ML model ID (required, numeric string e.g. "12345678")
  project_id : str  — GCP project ID (falls back to GOOGLE_PROJECT_ID env; informational)

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_ml_get_model

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required: firebase-admin Python SDK installed in environment
  - Required IAM role: roles/firebaseml.viewer or roles/firebase.viewer
  - model_id is the numeric ID returned by firebase_ml_list_models
  - tflite_model.uri is a signed GCS URL valid for model download
  - validation_error is non-empty if Firebase ML rejected the model file
"""

import json
import logging
import os
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials as fb_credentials

logger = logging.getLogger("snowdrop.firebase_ml_get_model")

TOOL_META = {
    "name": "firebase_ml_get_model",
    "description": (
        "Get details of a specific Firebase ML model including its download URI "
        "for TFLite deployment."
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


def firebase_ml_get_model(
    model_id: str,
    project_id: str | None = None,
) -> dict:
    """Get details of a specific Firebase ML model including its TFLite download URI.

    Args:
        model_id: The Firebase ML model identifier (numeric string).
            Obtain this from firebase_ml_list_models or the Firebase Console
            under Machine Learning → Custom.
        project_id: GCP project ID. Falls back to GOOGLE_PROJECT_ID env var
            if not supplied. This is used for informational output only; the
            firebase-admin SDK scopes the request via the initialized app's
            credentials.

    Returns:
        dict: Standard Snowdrop envelope::

            {
                "status": "ok",
                "data": {
                    "model_id": str,
                    "display_name": str,
                    "create_time": str,
                    "update_time": str,
                    "tags": list[str],
                    "tflite_model": {
                        "uri": str,
                        "size_bytes": int | None,
                        "hash": str | None
                    } | None,
                    "validation_error": str | None
                },
                "timestamp": "<ISO8601>"
            }

    Raises:
        RuntimeError: If no GCP credentials are available.

    Example:
        >>> result = firebase_ml_get_model(
        ...     model_id="12345678",
        ...     project_id="my-firebase-project",
        ... )
        >>> print(result["data"]["tflite_model"]["uri"])
        https://storage.googleapis.com/...
    """
    logger.info(
        "firebase_ml_get_model called: model_id=%s, project_id=%s",
        model_id,
        project_id,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")

    if not model_id:
        return _wrap("error", {"message": "model_id is required."})

    try:
        _get_fb_app()
        from firebase_admin import ml

        model = ml.get_model(model_id)

        # Extract TFLite model details; handle both SDK versions gracefully.
        tflite_info: dict | None = None
        validation_error: str | None = None

        try:
            tflite_model = getattr(model, "tflite_model", None)
            if tflite_model is not None:
                tflite_info = {
                    "uri": getattr(tflite_model, "gcs_tflite_uri", None),
                    "size_bytes": getattr(tflite_model, "size_bytes", None),
                    "hash": getattr(tflite_model, "model_hash", None),
                }
        except Exception as tflite_exc:
            logger.debug("Could not extract tflite_model details: %s", tflite_exc)

        # Newer SDK versions expose model_format instead of tflite_model.
        if tflite_info is None:
            try:
                model_format = getattr(model, "model_format", None)
                if model_format is not None:
                    tflite_info = {
                        "uri": getattr(model_format, "model_source", None),
                        "size_bytes": getattr(model_format, "size_bytes", None),
                        "hash": getattr(model_format, "model_hash", None),
                    }
            except Exception as fmt_exc:
                logger.debug("Could not extract model_format details: %s", fmt_exc)

        # Validation error surfaced when Firebase ML rejects the model file.
        try:
            validation_error = getattr(model, "validation_error", None) or None
        except Exception:
            pass

        result = {
            "model_id": getattr(model, "model_id", model_id),
            "display_name": getattr(model, "display_name", ""),
            "create_time": str(getattr(model, "create_time", "") or ""),
            "update_time": str(getattr(model, "update_time", "") or ""),
            "tags": list(getattr(model, "tags", []) or []),
            "tflite_model": tflite_info,
            "validation_error": validation_error,
        }

        logger.info(
            "firebase_ml_get_model succeeded: model_id=%s, display_name=%s",
            model_id,
            result["display_name"],
        )
        return _wrap("ok", result)

    except Exception as exc:
        logger.exception("Unexpected error in firebase_ml_get_model")
        return _wrap("error", {"message": str(exc)})
