"""
Executive Summary: Computes sovereign bond spreads over US Treasuries, constructs yield curves, and identifies inversions for Global South debt analysis.
Inputs: bonds (list[dict]: country, maturity_years, yield_pct, currency, credit_rating), benchmark_yields (dict: maturity → us_treasury_yield)
Outputs: spreads (list[dict]), yield_curve (list sorted by maturity), inversions (list), avg_spread (float)
MCP Tool Name: sovereign_debt_yield_curve
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sovereign_debt_yield_curve",
    "description": "Computes sovereign bond spreads over US Treasuries, builds yield curves, and identifies inversions for Global South debt analysis.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "bonds": {
                "type": "array",
                "description": "List of sovereign bond instruments",
                "items": {
                    "type": "object",
                    "properties": {
                        "country": {"type": "string"},
                        "maturity_years": {"type": "number", "description": "Years to maturity"},
                        "yield_pct": {"type": "number", "description": "Bond yield as percentage (e.g. 6.5 for 6.5%)"},
                        "currency": {"type": "string", "description": "ISO 4217 bond currency"},
                        "credit_rating": {"type": "string", "description": "S&P/Moody's/Fitch rating (e.g. BB, B+, CCC)"}
                    },
                    "required": ["country", "maturity_years", "yield_pct", "currency"]
                }
            },
            "benchmark_yields": {
                "type": "object",
                "description": "US Treasury yields keyed by maturity in years (e.g. {2: 4.5, 5: 4.3, 10: 4.2})",
                "additionalProperties": {"type": "number"}
            }
        },
        "required": ["bonds", "benchmark_yields"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "spreads": {"type": "array"},
                    "yield_curve": {"type": "array"},
                    "inversions": {"type": "array"},
                    "avg_spread": {"type": "number"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Credit rating risk tiers for context
CREDIT_RATING_TIER = {
    "AAA": "INVESTMENT_GRADE_PRIME",
    "AA+": "INVESTMENT_GRADE_HIGH", "AA": "INVESTMENT_GRADE_HIGH", "AA-": "INVESTMENT_GRADE_HIGH",
    "A+": "INVESTMENT_GRADE", "A": "INVESTMENT_GRADE", "A-": "INVESTMENT_GRADE",
    "BBB+": "INVESTMENT_GRADE_LOW", "BBB": "INVESTMENT_GRADE_LOW", "BBB-": "INVESTMENT_GRADE_LOW",
    "BB+": "SPECULATIVE", "BB": "SPECULATIVE", "BB-": "SPECULATIVE",
    "B+": "HIGHLY_SPECULATIVE", "B": "HIGHLY_SPECULATIVE", "B-": "HIGHLY_SPECULATIVE",
    "CCC+": "DISTRESSED", "CCC": "DISTRESSED", "CCC-": "DISTRESSED",
    "CC": "NEAR_DEFAULT", "C": "NEAR_DEFAULT",
    "D": "DEFAULT", "SD": "SELECTIVE_DEFAULT",
}

# Spread interpretation thresholds in basis points
SPREAD_RISK_THRESHOLDS = [
    (0, 100, "LOW_RISK"),
    (100, 300, "MODERATE_RISK"),
    (300, 600, "ELEVATED_RISK"),
    (600, 1000, "HIGH_RISK"),
    (1000, float("inf"), "DISTRESS_TERRITORY"),
]


def _interpolate_benchmark(maturity: float, benchmark_yields: dict[float, float]) -> float:
    """Linearly interpolate a US Treasury yield for a given maturity.

    Args:
        maturity: Bond maturity in years.
        benchmark_yields: Dictionary mapping maturity (years) to yield (%).

    Returns:
        float: Interpolated benchmark yield in percent.
    """
    sorted_maturities = sorted(benchmark_yields.keys())

    if maturity <= sorted_maturities[0]:
        return benchmark_yields[sorted_maturities[0]]
    if maturity >= sorted_maturities[-1]:
        return benchmark_yields[sorted_maturities[-1]]

    # Find bracketing maturities
    for i in range(len(sorted_maturities) - 1):
        lo = sorted_maturities[i]
        hi = sorted_maturities[i + 1]
        if lo <= maturity <= hi:
            weight = (maturity - lo) / (hi - lo)
            return benchmark_yields[lo] + weight * (benchmark_yields[hi] - benchmark_yields[lo])

    return benchmark_yields[sorted_maturities[-1]]


def _classify_spread(spread_bps: float) -> str:
    """Classify a spread in basis points into a risk category.

    Args:
        spread_bps: Spread over benchmark in basis points.

    Returns:
        str: Risk category label.
    """
    for lo, hi, label in SPREAD_RISK_THRESHOLDS:
        if lo <= spread_bps < hi:
            return label
    return "UNKNOWN"


def sovereign_debt_yield_curve(
    bonds: list[dict[str, Any]],
    benchmark_yields: dict[str, Any],
    **kwargs: Any
) -> dict[str, Any]:
    """Compute sovereign bond spreads and detect yield curve inversions.

    For each bond, interpolates the corresponding US Treasury yield at the
    same maturity and computes the spread in basis points. Builds a sorted
    yield curve and identifies inversions (adjacent longer-maturity bond with
    lower yield than shorter-maturity bond — a distress signal).

    Args:
        bonds: List of bond dicts. Each must have 'country' (str),
            'maturity_years' (float), 'yield_pct' (float), 'currency' (str).
            Optional: 'credit_rating' (str).
        benchmark_yields: Dict mapping maturity in years (as str or numeric keys)
            to US Treasury yield in percent. e.g. {"2": 4.5, "10": 4.2}.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Analysis results including spreads (list of dicts
              with country, maturity, yield, spread_bps, benchmark_yield,
              risk_category), yield_curve (sorted by maturity), inversions (list),
              avg_spread (float), country_summary (dict).
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        if not bonds:
            raise ValueError("bonds list must be non-empty")
        if not benchmark_yields:
            raise ValueError("benchmark_yields must be non-empty")

        # Normalize benchmark keys to float
        benchmark_float: dict[float, float] = {}
        for k, v in benchmark_yields.items():
            benchmark_float[float(k)] = float(v)

        spreads: list[dict[str, Any]] = []

        for bond in bonds:
            country = str(bond.get("country", "UNKNOWN")).strip()
            maturity = float(bond.get("maturity_years", 0))
            yield_pct = float(bond.get("yield_pct", 0))
            currency = str(bond.get("currency", "")).upper().strip()
            credit_rating = str(bond.get("credit_rating", "NR")).upper().strip()

            if maturity <= 0:
                logger.warning(f"Skipping bond with invalid maturity: {country} {maturity}y")
                continue

            # Interpolate benchmark yield at this maturity
            benchmark_yield = _interpolate_benchmark(maturity, benchmark_float)
            spread_pct = yield_pct - benchmark_yield
            spread_bps = round(spread_pct * 100, 2)  # 1% = 100 bps
            risk_category = _classify_spread(spread_bps)
            rating_tier = CREDIT_RATING_TIER.get(credit_rating, "UNKNOWN_RATING")

            spreads.append({
                "country": country,
                "maturity_years": maturity,
                "yield_pct": yield_pct,
                "benchmark_yield_pct": round(benchmark_yield, 4),
                "spread_pct": round(spread_pct, 4),
                "spread_bps": spread_bps,
                "currency": currency,
                "credit_rating": credit_rating,
                "rating_tier": rating_tier,
                "risk_category": risk_category,
            })

        if not spreads:
            raise ValueError("No valid bonds processed")

        # Build yield curve: sort by maturity
        yield_curve: list[dict[str, Any]] = sorted(spreads, key=lambda x: x["maturity_years"])

        # Detect inversions: adjacent point where longer maturity < shorter maturity yield
        inversions: list[dict[str, Any]] = []
        for i in range(len(yield_curve) - 1):
            short = yield_curve[i]
            long_ = yield_curve[i + 1]
            if long_["yield_pct"] < short["yield_pct"]:
                inversions.append({
                    "short_leg": {
                        "country": short["country"],
                        "maturity_years": short["maturity_years"],
                        "yield_pct": short["yield_pct"],
                    },
                    "long_leg": {
                        "country": long_["country"],
                        "maturity_years": long_["maturity_years"],
                        "yield_pct": long_["yield_pct"],
                    },
                    "inversion_magnitude_bps": round((short["yield_pct"] - long_["yield_pct"]) * 100, 2),
                    "signal": "INVERSION DETECTED — potential recession/distress signal",
                })

        # Average spread (simple mean across all bonds)
        avg_spread: float = round(sum(s["spread_bps"] for s in spreads) / len(spreads), 2)

        # Country summary: group by country
        country_summary: dict[str, Any] = {}
        for s in spreads:
            c = s["country"]
            if c not in country_summary:
                country_summary[c] = {"bonds": [], "avg_spread_bps": 0.0, "max_yield": 0.0}
            country_summary[c]["bonds"].append({
                "maturity_years": s["maturity_years"],
                "yield_pct": s["yield_pct"],
                "spread_bps": s["spread_bps"],
            })
            country_summary[c]["max_yield"] = max(country_summary[c]["max_yield"], s["yield_pct"])

        for c in country_summary:
            bond_spreads = [b["spread_bps"] for b in country_summary[c]["bonds"]]
            country_summary[c]["avg_spread_bps"] = round(sum(bond_spreads) / len(bond_spreads), 2)
            country_summary[c]["bond_count"] = len(bond_spreads)

        # Benchmark curve summary
        benchmark_curve = sorted(
            [{"maturity_years": m, "yield_pct": y} for m, y in benchmark_float.items()],
            key=lambda x: x["maturity_years"]
        )

        result: dict[str, Any] = {
            "spreads": spreads,
            "yield_curve": yield_curve,
            "inversions": inversions,
            "inversion_count": len(inversions),
            "avg_spread": avg_spread,
            "avg_spread_bps": avg_spread,
            "country_summary": country_summary,
            "benchmark_curve": benchmark_curve,
            "bond_count": len(spreads),
            "widest_spread": max(spreads, key=lambda x: x["spread_bps"]) if spreads else None,
            "tightest_spread": min(spreads, key=lambda x: x["spread_bps"]) if spreads else None,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"sovereign_debt_yield_curve failed: {e}")
        _log_lesson(f"sovereign_debt_yield_curve: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson/error entry to the shared lessons log.

    Args:
        message: Human-readable error or lesson description to append.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception as log_err:
        logger.warning(f"_log_lesson write failed: {log_err}")
