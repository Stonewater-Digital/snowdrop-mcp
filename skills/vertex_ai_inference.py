"""
Executive Summary
-----------------
Calls Vertex AI Gemini models for text generation, analysis, and embeddings via
the Vertex AI REST API. Uses explicit service account credentials only — no
gcloud CLI, no ADC, no google-cloud-aiplatform SDK (keeps dependencies minimal).
Supports Gemini 2.0 Flash, 1.5 Pro, and 1.5 Flash.

Credentials resolved in order:
  1. GOOGLE_SERVICE_ACCOUNT_JSON  — JSON string (cloud environments)
  2. GCP_SERVICE_ACCOUNT_FILE     — file path (HP local)

Inputs:
  action      : str   — "generate" | "analyze" | "embed"  (required)
  prompt      : str   — text prompt (required for generate/analyze)
  text        : str   — text to embed (required for embed)
  model       : str   — model ID (default "gemini-2.0-flash-exp")
  max_tokens  : int   — max output tokens (default 1024)
  temperature : float — sampling temperature 0.0-2.0 (default 0.7)
  project_id  : str   — GCP project (falls back to GOOGLE_PROJECT_ID env)
  region      : str   — Vertex AI region (default "us-central1")

Outputs:
  {"status": "ok"|"error", "data": {"text": str, "tokens_used": int, ...},
   "timestamp": "<ISO8601>"}

MCP Tool Name: vertex_ai_inference

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Required IAM role: roles/aiplatform.user
  - Required API: aiplatform.googleapis.com
  - Token auth: Bearer token obtained by refreshing SA credentials
  - No SDK dependency — pure REST via requests library
  - Default model "gemini-2.0-flash-exp" is fastest; use "gemini-1.5-pro" for complex tasks
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from config.models import resolve_model

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

SUPPORTED_MODELS = [
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
]

TOOL_META = {
    "name": "vertex_ai_inference",
    "description": (
        "Call Vertex AI Gemini models for text generation, analysis, or embeddings. "
        "Uses Vertex AI REST API with explicit service account credentials — no gcloud, no ADC. "
        "Supports gemini-2.0-flash-exp (fastest), gemini-1.5-pro (most capable), gemini-1.5-flash."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["generate", "analyze", "embed"],
                "description": "Operation: generate text, analyze input, or create embeddings.",
            },
            "prompt": {"type": "string", "description": "Text prompt (required for generate/analyze)."},
            "text": {"type": "string", "description": "Text to embed (required for embed)."},
            "model": {
                "type": "string",
                "default": "gemini-2.0-flash-exp",
                "description": "Gemini model ID.",
            },
            "max_tokens": {"type": "integer", "default": 1024},
            "temperature": {"type": "number", "default": 0.7},
            "project_id": {"type": "string", "description": "GCP project ID."},
            "region": {"type": "string", "default": "us-central1"},
        },
        "required": ["action"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "data", "timestamp"],
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _get_access_token() -> str:
    """Get a Bearer token from the service account — no gcloud, no ADC."""
    raw_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    creds = None
    if raw_json:
        try:
            info = json.loads(raw_json)
            creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        except (json.JSONDecodeError, ValueError):
            pass  # fall through to file-based auth
    if creds is None:
        key_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
        if not key_file:
            raise RuntimeError("Set GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE.")
        creds = service_account.Credentials.from_service_account_file(key_file, scopes=SCOPES)
    creds.refresh(Request())
    return creds.token


def _generate_content(
    project_id: str,
    region: str,
    model: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
) -> dict:
    token = _get_access_token()
    url = (
        f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}"
        f"/locations/{region}/publishers/google/models/{model}:generateContent"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": temperature,
        },
    }
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    candidates = data.get("candidates", [])
    text = ""
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
    usage = data.get("usageMetadata", {})
    return {
        "text": text,
        "model": model,
        "prompt_tokens": usage.get("promptTokenCount", 0),
        "output_tokens": usage.get("candidatesTokenCount", 0),
        "total_tokens": usage.get("totalTokenCount", 0),
    }


def _embed_text(project_id: str, region: str, text: str) -> dict:
    token = _get_access_token()
    model = "textembedding-gecko@003"
    url = (
        f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}"
        f"/locations/{region}/publishers/google/models/{model}:predict"
    )
    payload = {"instances": [{"content": text}]}
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    predictions = data.get("predictions", [])
    embedding = predictions[0].get("embeddings", {}).get("values", []) if predictions else []
    return {"embedding": embedding, "dimensions": len(embedding), "model": model}


def vertex_ai_inference(
    action: str,
    prompt: str = "",
    text: str = "",
    model: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    project_id: str = "",
    region: str = "us-central1",
) -> dict:
    """Call Vertex AI Gemini. Explicit SA credentials only — no gcloud, no ADC."""
    if model is None:
        _secretary = resolve_model("secretary")
        # resolve_model returns "provider/model_id"; Vertex needs bare model_id
        model = _secretary.split("/", 1)[-1]
    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        return _wrap("error", {"message": "project_id required (or set GOOGLE_PROJECT_ID)."})

    try:
        if action == "generate":
            if not prompt:
                return _wrap("error", {"message": "prompt is required for generate."})
            data = _generate_content(project_id, region, model, prompt, max_tokens, temperature)
            return _wrap("ok", data)

        elif action == "analyze":
            if not prompt:
                return _wrap("error", {"message": "prompt is required for analyze."})
            analysis_prompt = f"Analyze the following and provide structured insights:\n\n{prompt}"
            data = _generate_content(project_id, region, model, analysis_prompt, max_tokens, temperature)
            return _wrap("ok", data)

        elif action == "embed":
            if not text:
                return _wrap("error", {"message": "text is required for embed."})
            data = _embed_text(project_id, region, text)
            return _wrap("ok", data)

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'. Use: generate, analyze, embed."})

    except requests.HTTPError as exc:
        logger.exception("Vertex AI HTTP error")
        return _wrap("error", {"message": str(exc), "status_code": exc.response.status_code})
    except Exception as exc:
        logger.exception("vertex_ai_inference error")
        return _wrap("error", {"message": str(exc)})
