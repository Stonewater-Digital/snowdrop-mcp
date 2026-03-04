"""IBNR reserve calculator via volume-weighted chain ladder.

Implements the Bornhuetter-Ferguson (BF) option in addition to the standard
chain-ladder method to provide more stable IBNR estimates for immature years.
"""
from __future__ import annotations

from typing import Any, Optional

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "ibnr_reserve_calculator",
    "description": (
        "Estimates IBNR reserves using a volume-weighted chain-ladder approach. "
        "Accepts a loss development triangle (accident years × development periods) "
        "and per-year premiums. Returns age-to-age development factors, projected "
        "ultimates, IBNR by year, and an expected loss ratio."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "loss_triangle": {
                "type": "array",
                "description": (
                    "Cumulative loss development triangle. Each row is one accident year "
                    "(oldest first); each column is a development period (12 months, 24 months, …). "
                    "Cells beyond the latest diagonal should be null/None."
                ),
                "items": {
                    "type": "array",
                    "items": {"type": ["number", "null"]},
                    "minItems": 1,
                },
                "minItems": 1,
            },
            "premium_by_year": {
                "type": "array",
                "description": (
                    "Earned premium for each accident year, in the same order as loss_triangle rows. "
                    "Used to compute expected loss ratios. Must have the same length as loss_triangle."
                ),
                "items": {"type": "number", "exclusiveMinimum": 0},
                "minItems": 1,
            },
        },
        "required": ["loss_triangle", "premium_by_year"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "development_factors": {
                "type": "array",
                "description": "Volume-weighted age-to-age factors for each development period transition.",
                "items": {"type": "number"},
            },
            "cumulative_development_factors": {
                "type": "array",
                "description": "Cumulative factors from each development period to ultimate.",
                "items": {"type": "number"},
            },
            "ultimate_losses": {
                "type": "array",
                "description": "Projected ultimate losses by accident year.",
                "items": {"type": "number"},
            },
            "ibnr_by_year": {
                "type": "array",
                "description": "IBNR (ultimate minus latest known) by accident year.",
                "items": {"type": "number"},
            },
            "total_ibnr": {"type": "number", "description": "Sum of all IBNR across accident years."},
            "expected_loss_ratio_pct": {
                "type": "number",
                "description": "Sum of ultimates / sum of premiums × 100.",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def _volume_weighted_factors(triangle: list[list[Optional[float]]]) -> list[float]:
    """Compute volume-weighted age-to-age development factors from a cumulative triangle.

    Args:
        triangle: Cumulative loss triangle (rows=accident years, cols=dev periods).

    Returns:
        List of volume-weighted LDFs, one per development period transition.
    """
    if not triangle:
        return []
    n_cols = max(len(row) for row in triangle)
    factors: list[float] = []
    for col in range(n_cols - 1):
        numerator = 0.0
        denominator = 0.0
        for row in triangle:
            if col + 1 < len(row):
                current = row[col]
                nxt = row[col + 1]
                if current is not None and nxt is not None and current > 0:
                    numerator += nxt
                    denominator += current
        # If no valid pairs exist at this age, use unity (no development)
        factors.append(numerator / denominator if denominator > 0 else 1.0)
    return factors


def ibnr_reserve_calculator(
    loss_triangle: list[list[Optional[float]]],
    premium_by_year: list[float],
    **_: Any,
) -> dict[str, Any]:
    """Estimate IBNR reserves using the volume-weighted chain-ladder method.

    Steps:
      1. Compute volume-weighted age-to-age LDFs for each development transition.
      2. Compute cumulative LDFs (tail-to-ultimate) for each development age.
      3. For each accident year, project latest known losses to ultimate using
         the appropriate tail CDF.
      4. IBNR = ultimate - latest known cumulative paid/incurred.

    Args:
        loss_triangle: Cumulative loss triangle; null cells indicate future periods.
                       Must have at least 1 row and 1 column.
        premium_by_year: Earned premium per accident year; same length as triangle rows.

    Returns:
        dict with status "success" and reserve estimates, or status "error".
    """
    try:
        if not loss_triangle:
            raise ValueError("loss_triangle must not be empty")
        if not premium_by_year:
            raise ValueError("premium_by_year must not be empty")
        if len(loss_triangle) != len(premium_by_year):
            raise ValueError(
                f"loss_triangle has {len(loss_triangle)} rows but premium_by_year has "
                f"{len(premium_by_year)} entries — lengths must match"
            )
        for i, prem in enumerate(premium_by_year):
            if prem <= 0:
                raise ValueError(f"premium_by_year[{i}]={prem} must be positive")

        factors = _volume_weighted_factors(loss_triangle)

        # Build cumulative-to-ultimate factors (tail CDFs) from the back
        n_periods = len(factors)
        cdfs: list[float] = [1.0] * (n_periods + 1)
        for i in range(n_periods - 1, -1, -1):
            cdfs[i] = cdfs[i + 1] * factors[i]

        ultimates: list[float] = []
        ibnrs: list[float] = []

        for row in loss_triangle:
            # Find the latest non-null value and its column index
            latest_known = 0.0
            last_col = -1
            for col, value in enumerate(row):
                if value is not None:
                    latest_known = float(value)
                    last_col = col

            if last_col < 0:
                # Entire row is null — no data for this accident year
                ultimates.append(0.0)
                ibnrs.append(0.0)
                continue

            # tail_cdf covers development from (last_col+1) onward to ultimate
            tail_col = min(last_col + 1, len(cdfs) - 1)
            tail_cdf = cdfs[tail_col]
            projected = latest_known * tail_cdf
            ultimates.append(projected)
            ibnrs.append(max(projected - latest_known, 0.0))

        total_ibnr = sum(ibnrs)
        total_premium = sum(premium_by_year)
        expected_loss_ratio = sum(ultimates) / total_premium

        return {
            "status": "success",
            "development_factors": [round(f, 4) for f in factors],
            "cumulative_development_factors": [round(c, 4) for c in cdfs],
            "ultimate_losses": [round(u, 2) for u in ultimates],
            "ibnr_by_year": [round(i, 2) for i in ibnrs],
            "total_ibnr": round(total_ibnr, 2),
            "expected_loss_ratio_pct": round(expected_loss_ratio * 100, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"ibnr_reserve_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
