"""Build loss development triangle and summary statistics.

Constructs a cumulative paid loss development triangle from individual claim
records, computes volume-weighted age-to-age factors, selects a tail factor,
and derives cumulative-to-ultimate factors for each development age.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "claims_development_triangle",
    "description": (
        "Constructs a cumulative loss development triangle and computes volume-weighted "
        "age-to-age factors, tail factor, and cumulative-to-ultimate factors "
        "from a list of claim records with accident_year, development_year, and cumulative_paid fields."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "claims": {
                "type": "array",
                "description": (
                    "List of claim records. Each record must include: "
                    "accident_year (int), development_year (int, 1-indexed), "
                    "and cumulative_paid (number >= 0)."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "accident_year": {"type": "integer", "description": "Year of loss occurrence (e.g., 2020)."},
                        "development_year": {
                            "type": "integer",
                            "description": "Development period (1=12mo, 2=24mo, …).",
                            "minimum": 1,
                        },
                        "cumulative_paid": {
                            "type": "number",
                            "description": "Cumulative paid losses at this development age.",
                            "minimum": 0.0,
                        },
                    },
                    "required": ["accident_year", "development_year", "cumulative_paid"],
                },
                "minItems": 1,
            },
        },
        "required": ["claims"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "triangle": {
                "type": "object",
                "description": "Cumulative paid triangle keyed by accident_year string; each value is a list by dev period.",
            },
            "age_to_age_factors": {
                "type": "array",
                "description": "Volume-weighted age-to-age LDFs for each development transition.",
                "items": {"type": "number"},
            },
            "tail_factor": {
                "type": "number",
                "description": (
                    "Estimated tail factor beyond the last observed development period. "
                    "Derived as the product of the last two observed age-to-age factors."
                ),
            },
            "cumulative_to_ultimate_factors": {
                "type": "array",
                "description": "Cumulative LDF from each development age to ultimate (including tail).",
                "items": {"type": "number"},
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def claims_development_triangle(claims: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Build a cumulative loss development triangle and derive LDFs.

    Processing steps:
      1. Aggregate cumulative_paid into a triangle keyed by (accident_year, development_year).
      2. Compute volume-weighted age-to-age factors for each transition.
      3. Estimate a tail factor as the product of the last two observed factors
         (conservative; set to 1.0 if fewer than two factors are available).
      4. Compute cumulative-to-ultimate factors from each age to ultimate.

    Args:
        claims: List of dicts with accident_year (int), development_year (int, 1-indexed),
                and cumulative_paid (float >= 0). Duplicates for the same (ay, dy) are
                resolved by keeping the maximum value.

    Returns:
        dict with status "success" and triangle/factor data, or status "error".
    """
    try:
        if not claims:
            raise ValueError("claims must not be empty")

        # Validate required fields and types
        for idx, row in enumerate(claims):
            for field in ("accident_year", "development_year", "cumulative_paid"):
                if field not in row:
                    raise ValueError(f"claims[{idx}] is missing required field '{field}'")
            if int(row["development_year"]) < 1:
                raise ValueError(f"claims[{idx}].development_year must be >= 1, got {row['development_year']}")
            if float(row["cumulative_paid"]) < 0:
                raise ValueError(f"claims[{idx}].cumulative_paid must be >= 0, got {row['cumulative_paid']}")

        accident_years = sorted({int(r["accident_year"]) for r in claims})
        dev_periods = sorted({int(r["development_year"]) for r in claims})
        latest_dev = max(dev_periods)

        # Build triangle; resolve duplicates by keeping maximum cumulative value
        triangle: dict[int, list[float]] = {ay: [0.0] * latest_dev for ay in accident_years}
        for row in claims:
            ay = int(row["accident_year"])
            dy = int(row["development_year"]) - 1  # 0-indexed
            val = float(row["cumulative_paid"])
            if 0 <= dy < latest_dev:
                triangle[ay][dy] = max(triangle[ay][dy], val)

        # Volume-weighted age-to-age factors
        age_to_age: list[float] = []
        for age in range(latest_dev - 1):
            numer = 0.0
            denom = 0.0
            for ay in accident_years:
                current = triangle[ay][age]
                nxt = triangle[ay][age + 1]
                if current > 0 and nxt > 0:
                    numer += nxt
                    denom += current
            age_to_age.append(numer / denom if denom > 0 else 1.0)

        # Tail factor: product of last two observed factors (must each be >= 1.0)
        if len(age_to_age) >= 2:
            tail_factor = max(age_to_age[-2], 1.0) * max(age_to_age[-1], 1.0)
        elif len(age_to_age) == 1:
            tail_factor = max(age_to_age[-1], 1.0)
        else:
            tail_factor = 1.0

        # Cumulative-to-ultimate factors (each age to ultimate, including tail)
        # Build from the back: CDF[last] = tail_factor; CDF[i] = f[i] * CDF[i+1]
        n = len(age_to_age)
        cdf: list[float] = [1.0] * (n + 1)
        cdf[n] = tail_factor
        for i in range(n - 1, -1, -1):
            cdf[i] = age_to_age[i] * cdf[i + 1]

        return {
            "status": "success",
            "triangle": {str(k): v for k, v in triangle.items()},
            "age_to_age_factors": [round(f, 4) for f in age_to_age],
            "tail_factor": round(tail_factor, 4),
            "cumulative_to_ultimate_factors": [round(c, 4) for c in cdf],
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as exc:
        log_lesson(f"claims_development_triangle: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
