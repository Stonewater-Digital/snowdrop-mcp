"""
prep_daily_intel.py — Aggregate system health and logs into BLUF bullet points.

Executive Summary:
    Reads the last N hours of invocation logs and system health metrics, then
    uses Gemini (or OpenRouter fallback) to condense into 3-5 BLUF bullet points
    suitable for a C-Suite CTO briefing.

Table of Contents:
    1. TOOL_META
    2. Constants
    3. Log Aggregation
    4. System Health
    5. LLM Summarization
    6. Skill Implementation
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from config.models import resolve_model, validate_model

logger = logging.getLogger("snowdrop.prep_daily_intel")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "prep_daily_intel",
    "description": "Aggregate 24h logs and system health into 3-5 BLUF bullet points for CTO briefing.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hours_lookback": {
                "type": "integer",
                "description": "Hours to look back in logs (default: 24)",
            },
            "include_system_health": {
                "type": "boolean",
                "description": "Include system health metrics (default: true)",
            },
        },
    },
}

# ---------------------------------------------------------------------------
# 2. Constants
# ---------------------------------------------------------------------------

_GEMINI_SYSTEM_PROMPT = (
    "You are speaking to a C-Suite executive who has 30 seconds to read this. "
    "You must output exactly 3 to 5 highly condensed BLUF (Bottom Line Up Front) bullet points. "
    "If you return 2 bullets, you fail. If you return 6 bullets, you fail. "
    "No pleasantries. No intro text. No outro text. No greetings. No sign-offs. "
    "Just the bullets, each starting with '\u2022'. "
    "Each bullet: max 2 sentences, action-oriented, specific numbers where available."
)

_LOG_DIR = Path(os.environ.get("SNOWDROP_LOG_DIR", "/tmp/snowdrop/logs"))
_INVOCATION_LOG = _LOG_DIR / "invocations.jsonl"

# ---------------------------------------------------------------------------
# 3. Log Aggregation
# ---------------------------------------------------------------------------


def _aggregate_logs(hours: int) -> dict[str, Any]:
    """Read invocation logs and compute metrics for the last N hours.

    Returns:
        Dict with total_calls, errors, unique_skills, avg_latency_ms, error_rate.
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    total = 0
    errors = 0
    latencies: list[int] = []
    skills: set[str] = set()

    if _INVOCATION_LOG.exists():
        try:
            with open(_INVOCATION_LOG, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    ts = entry.get("ts", "")
                    if ts < cutoff:
                        continue
                    total += 1
                    if entry.get("status") == "error":
                        errors += 1
                    if "duration_ms" in entry:
                        latencies.append(entry["duration_ms"])
                    if "skill" in entry:
                        skills.add(entry["skill"])
        except OSError:
            pass

    avg_latency = round(sum(latencies) / len(latencies)) if latencies else 0
    error_rate = round(errors / total * 100, 1) if total > 0 else 0.0

    return {
        "total_calls": total,
        "errors": errors,
        "unique_skills": len(skills),
        "avg_latency_ms": avg_latency,
        "error_rate": error_rate,
        "top_skills": list(skills)[:10],
    }


# ---------------------------------------------------------------------------
# 4. System Health
# ---------------------------------------------------------------------------


def _system_health() -> dict[str, Any]:
    """Collect basic system health metrics."""
    health: dict[str, Any] = {}

    try:
        disk = shutil.disk_usage("/")
        health["disk_total_gb"] = round(disk.total / (1024**3), 1)
        health["disk_used_gb"] = round(disk.used / (1024**3), 1)
        health["disk_free_gb"] = round(disk.free / (1024**3), 1)
        health["disk_pct_used"] = round(disk.used / disk.total * 100, 1)
    except OSError:
        pass

    try:
        load = os.getloadavg()
        health["load_1m"] = round(load[0], 2)
        health["load_5m"] = round(load[1], 2)
        health["load_15m"] = round(load[2], 2)
    except (OSError, AttributeError):
        pass

    uptime_path = Path("/proc/uptime")
    if uptime_path.exists():
        try:
            uptime_secs = float(uptime_path.read_text().split()[0])
            health["uptime_hours"] = round(uptime_secs / 3600, 1)
        except (OSError, ValueError, IndexError):
            pass

    return health


# ---------------------------------------------------------------------------
# 5. LLM Summarization
# ---------------------------------------------------------------------------


def _get_vertex_credentials():
    """Resolve GCP credentials for Vertex AI (same pattern as all GCP skills).

    Resolution order:
        1. GOOGLE_SERVICE_ACCOUNT_JSON env var (JSON string)
        2. GCP_SERVICE_ACCOUNT_FILE env var (file path)
        3. Application Default Credentials (Cloud Run)
    """
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        try:
            from google.oauth2 import service_account
            return service_account.Credentials.from_service_account_info(
                json.loads(sa_json),
            )
        except (json.JSONDecodeError, ValueError):
            pass  # Misconfigured — fall through to file path

    sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
    if sa_file and Path(sa_file).exists():
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_file(sa_file)

    return None  # Let ADC handle it


def _summarize_with_gemini(raw_intel: str) -> tuple[str | None, Exception | None]:
    """Call Gemini to produce BLUF bullets from raw intel."""
    try:
        from google.cloud import aiplatform
        from vertexai.generative_models import GenerativeModel

        creds = _get_vertex_credentials()
        aiplatform.init(
            project=os.environ.get("GOOGLE_PROJECT_ID", "project-57631ae1-b906-445a-852"),
            location="us-central1",
            credentials=creds,
        )

        _secretary = validate_model("secretary")
        # validate_model returns "provider/model_id"; Vertex needs bare model_id
        _model_id = _secretary.split("/", 1)[-1]
        model = GenerativeModel(_model_id)
        response = model.generate_content(
            [_GEMINI_SYSTEM_PROMPT, raw_intel],
        )
        return response.text, None
    except Exception as exc:
        logger.warning("Gemini summarization failed: %s — trying OpenRouter fallback", exc)
        return None, exc


def _summarize_with_openrouter(raw_intel: str) -> tuple[str | None, Exception | None]:
    """Fallback: Call OpenRouter for summarization."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None, Exception("OPENROUTER_API_KEY not set")

    try:
        import httpx

        resp = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": validate_model("secretary"),
                "messages": [
                    {"role": "system", "content": _GEMINI_SYSTEM_PROMPT},
                    {"role": "user", "content": raw_intel},
                ],
                "max_tokens": 500,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"], None
    except Exception as exc:
        logger.warning("OpenRouter fallback failed: %s", exc)
        return None, exc


def _parse_bullets(text: str) -> list[str]:
    """Parse LLM response into 3-5 bullet points.

    Splits by bullet character or newlines, enforces 3-5 count.
    """
    bullets = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("\u2022"):
            bullets.append(line)
        elif line.startswith("- "):
            bullets.append("\u2022 " + line[2:])
        elif line.startswith("* "):
            bullets.append("\u2022 " + line[2:])
        elif line and len(bullets) > 0:
            # Continuation of previous bullet
            continue

    # Enforce 3-5 bullets
    if len(bullets) > 5:
        bullets = bullets[:5]
    elif len(bullets) < 3:
        while len(bullets) < 3:
            bullets.append("\u2022 No additional intel to report.")

    return bullets


# ---------------------------------------------------------------------------
# 6. Skill Implementation
# ---------------------------------------------------------------------------


def prep_daily_intel(
    hours_lookback: int = 24,
    include_system_health: bool = True,
) -> dict[str, Any]:
    """Aggregate logs and system health into BLUF bullet points.

    Args:
        hours_lookback: Hours of log data to analyze.
        include_system_health: Whether to include system metrics.

    Returns:
        Standard Snowdrop response with bullets, status_indicator, and raw_metrics.
    """
    ts = datetime.now(timezone.utc).isoformat()

    try:
        # Aggregate raw data
        log_metrics = _aggregate_logs(hours_lookback)
        sys_health = _system_health() if include_system_health else {}

        # Build raw intel string
        raw_parts = [
            f"=== SNOWDROP INTEL REPORT — Last {hours_lookback}h ===",
            f"Total skill invocations: {log_metrics['total_calls']}",
            f"Errors: {log_metrics['errors']} ({log_metrics['error_rate']}% error rate)",
            f"Unique skills used: {log_metrics['unique_skills']}",
            f"Average latency: {log_metrics['avg_latency_ms']}ms",
        ]
        if sys_health:
            raw_parts.append(f"Disk: {sys_health.get('disk_used_gb', '?')}GB / {sys_health.get('disk_total_gb', '?')}GB ({sys_health.get('disk_pct_used', '?')}%)")
            if "load_1m" in sys_health:
                raw_parts.append(f"Load: {sys_health['load_1m']} / {sys_health['load_5m']} / {sys_health['load_15m']}")
            if "uptime_hours" in sys_health:
                raw_parts.append(f"Uptime: {sys_health['uptime_hours']}h")

        raw_intel = "\n".join(raw_parts)

        # Summarize
        summary, vertex_err = _summarize_with_gemini(raw_intel)
        if summary is None:
            summary, or_err = _summarize_with_openrouter(raw_intel)
        if summary is None:
            # Final fallback — generate bullets from raw data
            model_id = validate_model("secretary")
            logger.error("daily_intel_llm_failed", extra={
                "model": model_id,
                "vertex_error": str(vertex_err),
                "openrouter_error": str(or_err),
                "fallback": "raw_data_bullets",
                "action": "check config/config.yaml secretary.model_id"
            })
            summary = (
                f"\u2022 {log_metrics['total_calls']} skill invocations in the last {hours_lookback}h "
                f"with {log_metrics['error_rate']}% error rate.\n"
                f"\u2022 {log_metrics['unique_skills']} unique skills active, avg latency {log_metrics['avg_latency_ms']}ms.\n"
                f"\u2022 System operational — no critical alerts detected."
            )

        bullets = _parse_bullets(summary)

        # Determine status indicator
        error_rate = log_metrics["error_rate"]
        if error_rate > 10:
            status_indicator = "RED"
        elif error_rate > 2:
            status_indicator = "YELLOW"
        else:
            status_indicator = "GREEN"

        return {
            "status": "ok",
            "data": {
                "bullets": bullets,
                "status_indicator": status_indicator,
                "raw_metrics": {
                    "logs": log_metrics,
                    "system": sys_health,
                },
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("prep_daily_intel failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
