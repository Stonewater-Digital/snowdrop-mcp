"""Insurance leverage and capacity utilization calculator.

Computes key balance-sheet leverage ratios used by rating agencies (A.M. Best,
S&P, Moody's) and regulators to assess insurer financial strength.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

# A.M. Best benchmark: NWP/surplus > 3.0x is a red flag; > 2.0x warrants review.
# A.M. Best benchmark: liabilities/surplus > 5.0x for long-tail lines is concerning.
_BENCHMARK_NWP_TO_SURPLUS_WARNING = 3.0
_BENCHMARK_LIABILITIES_TO_SURPLUS_WARNING = 5.0

TOOL_META: dict[str, Any] = {
    "name": "insurance_leverage_calculator",
    "description": (
        "Computes leverage and capacity utilization metrics for P&C insurers: "
        "net written premium-to-surplus, liabilities-to-surplus, investment leverage, "
        "and capacity headroom vs. A.M. Best benchmarks."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_written_premium": {
                "type": "number",
                "description": "Annual net written premium (after cessions). Must be >= 0.",
                "minimum": 0.0,
            },
            "policyholder_surplus": {
                "type": "number",
                "description": "Statutory policyholder surplus (net assets). Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "total_liabilities": {
                "type": "number",
                "description": "Total statutory liabilities (loss reserves + unearned premium + other). Must be >= 0.",
                "minimum": 0.0,
            },
            "invested_assets": {
                "type": "number",
                "description": "Total invested assets at market value. Must be >= 0.",
                "minimum": 0.0,
            },
            "nwp_to_surplus_benchmark": {
                "type": "number",
                "description": (
                    "NWP-to-surplus ratio threshold above which capacity is flagged as stretched. "
                    "A.M. Best guideline is 3.0x; default 3.0."
                ),
                "default": 3.0,
                "exclusiveMinimum": 0.0,
            },
        },
        "required": [
            "net_written_premium",
            "policyholder_surplus",
            "total_liabilities",
            "invested_assets",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "nwp_to_surplus_ratio": {
                "type": "number",
                "description": "NWP / surplus. A.M. Best red flag > 3.0x.",
            },
            "liabilities_to_surplus_ratio": {
                "type": "number",
                "description": "Total liabilities / surplus. Measures balance-sheet leverage.",
            },
            "investment_leverage": {
                "type": "number",
                "description": "Invested assets / surplus. Measures asset-side risk.",
            },
            "capacity_headroom": {
                "type": "number",
                "description": "Additional premium the insurer can write before reaching the benchmark limit.",
            },
            "capacity_utilization_pct": {
                "type": "number",
                "description": "NWP / (surplus × benchmark) × 100.",
            },
            "leverage_flag": {
                "type": "string",
                "enum": ["within_benchmark", "approaching_limit", "exceeds_benchmark"],
                "description": "Capacity assessment vs. the NWP/surplus benchmark.",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def insurance_leverage_calculator(
    net_written_premium: float,
    policyholder_surplus: float,
    total_liabilities: float,
    invested_assets: float,
    nwp_to_surplus_benchmark: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute insurer leverage and capacity utilization metrics.

    Key ratios:
      NWP/surplus         — premium leverage; A.M. Best flags > 3.0x
      liabilities/surplus — balance-sheet leverage
      invested assets/surplus — asset leverage
      capacity_headroom   = (benchmark × surplus) - NWP

    Args:
        net_written_premium: Annual NWP after cessions. Must be >= 0.
        policyholder_surplus: Statutory surplus. Must be > 0.
        total_liabilities: Total statutory liabilities. Must be >= 0.
        invested_assets: Total invested assets at market value. Must be >= 0.
        nwp_to_surplus_benchmark: NWP/surplus warning threshold; default 3.0.

    Returns:
        dict with status "success" and leverage metrics, or status "error".
    """
    try:
        if policyholder_surplus <= 0:
            raise ValueError(f"policyholder_surplus must be positive, got {policyholder_surplus}")
        if net_written_premium < 0:
            raise ValueError(f"net_written_premium must be >= 0, got {net_written_premium}")
        if total_liabilities < 0:
            raise ValueError(f"total_liabilities must be >= 0, got {total_liabilities}")
        if invested_assets < 0:
            raise ValueError(f"invested_assets must be >= 0, got {invested_assets}")
        if nwp_to_surplus_benchmark <= 0:
            raise ValueError(f"nwp_to_surplus_benchmark must be positive, got {nwp_to_surplus_benchmark}")

        nwp_to_surplus = net_written_premium / policyholder_surplus
        liabilities_to_surplus = total_liabilities / policyholder_surplus
        investment_leverage = invested_assets / policyholder_surplus

        capacity_limit = policyholder_surplus * nwp_to_surplus_benchmark
        capacity_utilization = net_written_premium / capacity_limit
        capacity_headroom = max(capacity_limit - net_written_premium, 0.0)

        if nwp_to_surplus >= nwp_to_surplus_benchmark:
            leverage_flag = "exceeds_benchmark"
        elif nwp_to_surplus >= nwp_to_surplus_benchmark * 0.85:
            leverage_flag = "approaching_limit"
        else:
            leverage_flag = "within_benchmark"

        return {
            "status": "success",
            "nwp_to_surplus_ratio": round(nwp_to_surplus, 3),
            "liabilities_to_surplus_ratio": round(liabilities_to_surplus, 3),
            "investment_leverage": round(investment_leverage, 3),
            "capacity_headroom": round(capacity_headroom, 2),
            "capacity_utilization_pct": round(capacity_utilization * 100, 2),
            "leverage_flag": leverage_flag,
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"insurance_leverage_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
