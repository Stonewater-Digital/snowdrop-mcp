"""Agent churn analytics with cohort tracking."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "churn_analyzer",
    "description": "Analyzes churn patterns, cohort retention, and at-risk agents.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agents": {
                "type": "array",
                "items": {"type": "object"},
                "description": (
                    "Agent records with agent_id, signup_date, last_active_date, total_spend, and tier."
                ),
            },
            "analysis_date": {
                "type": "string",
                "description": "ISO timestamp used to determine churn windows.",
            },
            "churn_window_days": {
                "type": "integer",
                "description": "Days of inactivity before an agent is considered churned.",
                "default": 30,
            },
        },
        "required": ["agents", "analysis_date"],
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


def churn_analyzer(
    agents: list[dict[str, Any]],
    analysis_date: str,
    churn_window_days: int = 30,
    **_: Any,
) -> dict[str, Any]:
    """Evaluate churn for Watering Hole agents."""
    try:
        if not isinstance(agents, list):
            raise ValueError("agents must be a list")
        if churn_window_days <= 0:
            raise ValueError("churn_window_days must be positive")

        analysis_dt = _parse_datetime(analysis_date, "analysis_date")
        cohorts: dict[str, dict[str, float]] = {}
        churned_count = 0
        at_risk: list[dict[str, Any]] = []
        lifetime_days: list[int] = []

        for record in agents:
            if not isinstance(record, dict):
                raise ValueError("Each agent entry must be a dict")
            try:
                agent_id = str(record["agent_id"])
                signup_dt = _parse_datetime(record["signup_date"], "signup_date")
                last_active_dt = _parse_datetime(record["last_active_date"], "last_active_date")
            except KeyError as missing:
                raise ValueError(f"Missing field: {missing.args[0]}") from missing

            cohort_key = signup_dt.strftime("%Y-%m")
            cohort_stats = cohorts.setdefault(
                cohort_key,
                {"total": 0, "retained": 0, "churned": 0},
            )
            cohort_stats["total"] += 1

            days_since_active = max((analysis_dt - last_active_dt).days, 0)
            is_churned = days_since_active > churn_window_days
            if is_churned:
                cohort_stats["churned"] += 1
                churned_count += 1
            else:
                cohort_stats["retained"] += 1

            spend = float(record.get("total_spend", 0.0))
            tier = str(record.get("tier", "unknown"))
            low_spend = spend < 100.0
            infrequent = days_since_active > churn_window_days / 2
            if not is_churned and (low_spend or infrequent):
                at_risk.append(
                    {
                        "agent_id": agent_id,
                        "tier": tier,
                        "days_since_active": days_since_active,
                        "total_spend": round(spend, 2),
                        "risk_factors": [
                            label
                            for flag, label in [
                                (low_spend, "low_spend"),
                                (infrequent, "infrequent_usage"),
                            ]
                            if flag
                        ],
                    }
                )

            lifetime_days.append(max((last_active_dt - signup_dt).days, 0))

        total_agents = len(agents)
        overall_churn_rate = (churned_count / total_agents) if total_agents else 0.0

        cohort_retention = {
            cohort: {
                "size": stats["total"],
                "retained_pct": round(
                    stats["retained"] / stats["total"], 4
                )
                if stats["total"]
                else 0.0,
                "churn_rate": round(
                    stats["churned"] / stats["total"], 4
                )
                if stats["total"]
                else 0.0,
            }
            for cohort, stats in cohorts.items()
        }

        avg_lifetime = sum(lifetime_days) / len(lifetime_days) if lifetime_days else 0.0
        result = {
            "overall_churn_rate": round(overall_churn_rate, 4),
            "cohort_retention": cohort_retention,
            "at_risk_agents": at_risk,
            "avg_lifetime_days": round(avg_lifetime, 2),
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("churn_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_datetime(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO datetime string")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:  # noqa: B904
        raise ValueError(f"Invalid {field_name}: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
