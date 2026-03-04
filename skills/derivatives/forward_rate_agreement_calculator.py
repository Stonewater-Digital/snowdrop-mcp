"""Forward rate agreement settlement calculator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "forward_rate_agreement_calculator",
    "description": "Calculates FRA settlement amounts given contracted and market rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number", "description": "FRA notional amount. Must be > 0."},
            "fra_rate_pct": {"type": "number", "description": "Contracted FRA rate as a percentage."},
            "settlement_rate_pct": {"type": "number", "description": "LIBOR/SOFR fixing rate at settlement, as a percentage."},
            "contract_period_days": {"type": "integer", "description": "Length of the FRA contract period in days."},
            "settlement_delay_days": {"type": "integer", "default": 2, "description": "Settlement lag in days (default 2 for T+2)."},
            "day_count_convention": {
                "type": "string",
                "enum": ["actual_360", "actual_365"],
                "default": "actual_360",
                "description": "Day count convention for accrual fraction.",
            },
        },
        "required": [
            "notional",
            "fra_rate_pct",
            "settlement_rate_pct",
            "contract_period_days",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "settlement_amount": {"type": "number"},
                    "discounted_settlement": {"type": "number"},
                    "buyer_receives": {"type": "boolean"},
                    "accrual_fraction": {"type": "number"},
                    "rate_differential_bps": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def forward_rate_agreement_calculator(
    notional: float,
    fra_rate_pct: float,
    settlement_rate_pct: float,
    contract_period_days: int,
    settlement_delay_days: int = 2,
    day_count_convention: str = "actual_360",
    **_: Any,
) -> dict[str, Any]:
    """Return FRA settlement value (discounted).

    FRA settlement formula (ISDA):
        gross_settlement = N * (L - R) * alpha / (1 + L * alpha)
    where:
        N = notional
        L = settlement (LIBOR) rate
        R = FRA contract rate
        alpha = contract_period_days / day_count_basis

    The settlement is discounted back from period end to settlement date
    using the settlement rate.

    Args:
        notional: Notional amount (must be > 0).
        fra_rate_pct: Contracted FRA rate as a percentage.
        settlement_rate_pct: Market fixing rate as a percentage.
        contract_period_days: Length of FRA contract period in days.
        settlement_delay_days: Settlement lag in days.
        day_count_convention: 'actual_360' or 'actual_365'.

    Returns:
        dict with settlement_amount (undiscounted), discounted_settlement,
        buyer_receives, accrual_fraction, rate_differential_bps.
    """
    try:
        if notional <= 0:
            raise ValueError("notional must be positive")
        if contract_period_days <= 0:
            raise ValueError("contract_period_days must be positive")

        denom = 360 if day_count_convention == "actual_360" else 365
        accrual_fraction = contract_period_days / denom
        fra_rate = fra_rate_pct / 100.0
        settlement_rate = settlement_rate_pct / 100.0
        rate_diff = settlement_rate - fra_rate

        # ISDA FRA settlement: discounted at settlement rate for the contract period
        gross_settlement = notional * rate_diff * accrual_fraction
        discount_factor = 1.0 + settlement_rate * accrual_fraction
        if discount_factor == 0:
            raise ValueError("Settlement rate produces zero discount denominator")
        discounted_settlement = gross_settlement / discount_factor

        # Buyer (long FRA) receives when settlement rate > FRA rate
        buyer_receives = discounted_settlement > 0

        data = {
            "settlement_amount": round(gross_settlement, 2),
            "discounted_settlement": round(discounted_settlement, 2),
            "buyer_receives": buyer_receives,
            "accrual_fraction": round(accrual_fraction, 6),
            "rate_differential_bps": round(rate_diff * 10000, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"forward_rate_agreement_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
