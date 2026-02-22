"""Monitor vendor SLA compliance."""
from __future__ import annotations

import statistics
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "vendor_sla_monitor",
    "description": "Evaluates uptime and latency metrics vs SLA targets for each vendor.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "vendors": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["vendors"],
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


def vendor_sla_monitor(vendors: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return SLA scorecards for each vendor."""
    try:
        scorecards = []
        for vendor in vendors:
            checks = vendor.get("health_checks", [])
            if not checks:
                continue
            successes = [check for check in checks if check.get("status") == "ok"]
            uptime_pct = len(successes) / len(checks) * 100
            latencies = [float(check.get("latency_ms", 0.0)) for check in checks]
            avg_latency = statistics.mean(latencies)
            p99_latency = sorted(latencies)[-1] if latencies else 0.0
            sla_met = uptime_pct >= float(vendor.get("sla_target_pct", 99.0))
            scorecards.append(
                {
                    "name": vendor.get("name"),
                    "uptime_pct": round(uptime_pct, 2),
                    "avg_latency_ms": round(avg_latency, 2),
                    "p99_latency_ms": round(p99_latency, 2),
                    "sla_met": sla_met,
                }
            )
        data = {"vendors": scorecards}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("vendor_sla_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
