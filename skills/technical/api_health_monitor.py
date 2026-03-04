"""Check health of Snowdrop's external API dependencies."""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

import requests

TOOL_META: dict[str, Any] = {
    "name": "api_health_monitor",
    "description": "Performs lightweight health checks and scores availability.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "endpoints": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["endpoints"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "reports": {"type": "array", "items": {"type": "object"}},
                    "health_score": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def api_health_monitor(endpoints: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Hit each configured endpoint with a HEAD request and score health."""

    try:
        if not endpoints:
            raise ValueError("endpoints list cannot be empty")
        reports: list[dict[str, Any]] = []
        for endpoint in endpoints:
            url = endpoint.get("url")
            expected = int(endpoint.get("expected_status", 200))
            timeout_ms = int(endpoint.get("timeout_ms", 2000))
            if not url:
                raise ValueError("Each endpoint requires a url")
            name = endpoint.get("name", url)
            start = time.monotonic()
            healthy = False
            status_code: int | None = None
            error: str | None = None
            try:
                response = requests.head(url, timeout=timeout_ms / 1000)
                status_code = response.status_code
                healthy = status_code == expected
            except requests.RequestException as exc:
                error = str(exc)
            latency_ms = round((time.monotonic() - start) * 1000, 2)
            reports.append(
                {
                    "name": name,
                    "url": url,
                    "status_code": status_code,
                    "latency_ms": latency_ms,
                    "healthy": healthy,
                    "error": error,
                }
            )

        health_score = round(
            100 * sum(1 for report in reports if report["healthy"]) / len(reports), 2
        )
        return {
            "status": "success",
            "data": {"reports": reports, "health_score": health_score},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("api_health_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
