"""Monthly recurring revenue analytics for the Watering Hole."""
from __future__ import annotations

from datetime import date, datetime, timezone, timedelta
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mrr_calculator",
    "description": "Calculates MRR components and growth for Watering Hole subscriptions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sions": {
                "type": "array",
                "items": {"type": "object"},
                "description": (
                    "Subscription entries containing agent_id, plan, monthly_rate, status, and"
                    " start_date (ISO 8601)."
                ),
            },
            "analysis_date": {
                "type": "string",
                "description": "ISO date overriding today's date for month selection.",
            },
            "previous_month_mrr": {
                "type": "number",
                "description": "Optional prior month MRR to compute MoM growth.",
            },
        },
        "required": ["sions"],
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


def mrr_calculator(
    sions: list[dict[str, Any]],
    analysis_date: str | None = None,
    previous_month_mrr: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Compute detailed MRR decomposition and growth metrics."""
    try:
        if not isinstance(sions, list):
            raise ValueError("sions must be a list of subscription entries")

        analysis_day = _resolve_analysis_date(analysis_date)
        month_start = analysis_day.replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)

        total_mrr = 0.0
        new_mrr = 0.0
        churned_mrr = 0.0
        expansion_mrr = 0.0
        contraction_mrr = 0.0
        prev_baseline = 0.0
        status_breakdown: dict[str, int] = {"active": 0, "paused": 0, "churned": 0}

        for entry in sions:
            if not isinstance(entry, dict):
                raise ValueError("Each subscription entry must be a dict")
            if "monthly_rate" not in entry or "status" not in entry or "start_date" not in entry:
                raise ValueError("monthly_rate, status, and start_date are required fields")

            rate = _to_float(entry["monthly_rate"], "monthly_rate")
            prev_rate = _to_float(entry.get("previous_month_rate", rate), "previous_month_rate")
            status = str(entry.get("status", "active")).lower()
            start_date = _parse_date_field(entry["start_date"], "start_date")

            prev_baseline += max(prev_rate, 0.0)
            if status in status_breakdown:
                status_breakdown[status] += 1

            if status == "active":
                total_mrr += max(rate, 0.0)
                if month_start <= start_date < next_month:
                    new_mrr += max(rate, 0.0)
                diff = rate - prev_rate
                if diff > 0:
                    expansion_mrr += diff
                elif diff < 0:
                    contraction_mrr += abs(diff)
            elif status == "churned":
                churned_mrr += max(prev_rate, rate, 0.0)

        net_new_mrr = new_mrr + expansion_mrr - churned_mrr - contraction_mrr
        baseline = previous_month_mrr if previous_month_mrr is not None else prev_baseline
        growth_rate = ((total_mrr - baseline) / baseline) if baseline > 0 else None

        result = {
            "analysis_month": month_start.strftime("%Y-%m"),
            "total_mrr": round(total_mrr, 2),
            "new_mrr": round(new_mrr, 2),
            "churned_mrr": round(churned_mrr, 2),
            "expansion_mrr": round(expansion_mrr, 2),
            "contraction_mrr": round(contraction_mrr, 2),
            "net_new_mrr": round(net_new_mrr, 2),
            "month_over_month_growth_rate": round(growth_rate, 4) if growth_rate is not None else None,
            "status_breakdown": status_breakdown,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("mrr_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _resolve_analysis_date(value: str | None) -> date:
    if value is None:
        return datetime.now(timezone.utc).date()
    return _parse_date_field(value, "analysis_date")


def _parse_date_field(value: Any, field_name: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO date string")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:  # noqa: B904
        raise ValueError(f"Invalid {field_name}: {value}") from exc
    return parsed.date()


def _to_float(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:  # noqa: B904
        raise ValueError(f"{field_name} must be numeric") from exc


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
