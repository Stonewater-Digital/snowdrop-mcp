"""
Executive Summary: Aggregates CRE cap rates from comparable sales, grouping averages by asset class and market.
Inputs: comparables (list of dicts: property_name, noi, sale_price, asset_class, market)
Outputs: dict with individual_rates (list), by_asset_class (dict), by_market (dict), overall_avg (float)
MCP Tool Name: cre_cap_rate_aggregator
"""
import os
import logging
from collections import defaultdict
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cre_cap_rate_aggregator",
    "description": (
        "Aggregates capitalization rates from a list of comparable CRE sales. "
        "Computes individual cap rates (NOI / sale_price), then averages by "
        "asset class (office, retail, multifamily, etc.) and by market (MSA). "
        "Returns overall market average and outlier flags."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "comparables": {
                "type": "array",
                "description": "List of comparable sales.",
                "items": {
                    "type": "object",
                    "properties": {
                        "property_name": {"type": "string"},
                        "noi":           {"type": "number"},
                        "sale_price":    {"type": "number"},
                        "asset_class":   {"type": "string"},
                        "market":        {"type": "string"}
                    },
                    "required": ["property_name", "noi", "sale_price", "asset_class", "market"]
                }
            }
        },
        "required": ["comparables"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "individual_rates": {"type": "array"},
                    "by_asset_class":   {"type": "object"},
                    "by_market":        {"type": "object"},
                    "overall_avg":      {"type": "number"},
                    "outliers":         {"type": "array"}
                },
                "required": ["individual_rates", "by_asset_class", "by_market", "overall_avg"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Outlier detection: flag if cap rate deviates > 2 std devs from mean
OUTLIER_STD_MULTIPLIER: float = 2.0


def cre_cap_rate_aggregator(
    comparables: list[dict],
    **kwargs: Any
) -> dict:
    """Compute and aggregate capitalization rates from comparable CRE sales.

    cap_rate = NOI / sale_price for each comparable. Groups and averages by
    asset_class (e.g., 'multifamily', 'office') and market (e.g., 'Austin-TX').
    Flags statistical outliers using a 2-standard-deviation rule.

    Args:
        comparables: List of sale comp dicts with property_name, noi, sale_price,
            asset_class, and market fields.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (individual_rates, by_asset_class, by_market,
        overall_avg, comp_count, outliers), timestamp.

    Raises:
        ValueError: If comparables is empty or any required field is missing.
    """
    try:
        if not comparables:
            raise ValueError("comparables list cannot be empty.")

        individual_rates: list[dict] = []
        all_cap_rates: list[float] = []

        for i, comp in enumerate(comparables):
            for field in ("property_name", "noi", "sale_price", "asset_class", "market"):
                if field not in comp:
                    raise ValueError(f"comparable[{i}] missing required field '{field}'.")

            noi = float(comp["noi"])
            sale_price = float(comp["sale_price"])

            if sale_price <= 0:
                raise ValueError(
                    f"comparable[{i}] '{comp['property_name']}' has non-positive sale_price={sale_price}."
                )
            if noi < 0:
                logger.warning(
                    "comparable[%d] '%s' has negative NOI=%.2f; cap rate will be negative.",
                    i, comp["property_name"], noi
                )

            cap_rate = noi / sale_price
            all_cap_rates.append(cap_rate)

            individual_rates.append({
                "property_name": str(comp["property_name"]),
                "noi": round(noi, 2),
                "sale_price": round(sale_price, 2),
                "asset_class": str(comp["asset_class"]).lower().strip(),
                "market": str(comp["market"]).strip(),
                "cap_rate": round(cap_rate, 6),
                "cap_rate_pct": round(cap_rate * 100, 3)
            })

        # Overall statistics
        n = len(all_cap_rates)
        overall_avg: float = sum(all_cap_rates) / n
        variance = sum((r - overall_avg) ** 2 for r in all_cap_rates) / n
        std_dev = variance ** 0.5

        # Outlier detection
        outliers: list[dict] = []
        outlier_threshold = OUTLIER_STD_MULTIPLIER * std_dev
        for entry in individual_rates:
            deviation = abs(entry["cap_rate"] - overall_avg)
            if deviation > outlier_threshold and std_dev > 0:
                entry["outlier"] = True
                outliers.append({
                    "property_name": entry["property_name"],
                    "cap_rate_pct": entry["cap_rate_pct"],
                    "deviation_from_mean_pct": round((entry["cap_rate"] - overall_avg) * 100, 3)
                })
            else:
                entry["outlier"] = False

        # Aggregate by asset class
        by_asset_class_raw: dict[str, list[float]] = defaultdict(list)
        for entry in individual_rates:
            by_asset_class_raw[entry["asset_class"]].append(entry["cap_rate"])

        by_asset_class: dict[str, dict] = {}
        for cls, rates in by_asset_class_raw.items():
            by_asset_class[cls] = {
                "avg_cap_rate_pct": round(sum(rates) / len(rates) * 100, 3),
                "min_cap_rate_pct": round(min(rates) * 100, 3),
                "max_cap_rate_pct": round(max(rates) * 100, 3),
                "count": len(rates)
            }

        # Aggregate by market
        by_market_raw: dict[str, list[float]] = defaultdict(list)
        for entry in individual_rates:
            by_market_raw[entry["market"]].append(entry["cap_rate"])

        by_market: dict[str, dict] = {}
        for mkt, rates in by_market_raw.items():
            by_market[mkt] = {
                "avg_cap_rate_pct": round(sum(rates) / len(rates) * 100, 3),
                "min_cap_rate_pct": round(min(rates) * 100, 3),
                "max_cap_rate_pct": round(max(rates) * 100, 3),
                "count": len(rates)
            }

        result: dict = {
            "individual_rates": individual_rates,
            "by_asset_class": by_asset_class,
            "by_market": by_market,
            "overall_avg": round(overall_avg, 6),
            "overall_avg_pct": round(overall_avg * 100, 3),
            "std_dev_pct": round(std_dev * 100, 3),
            "comp_count": n,
            "outliers": outliers,
            "outlier_count": len(outliers)
        }

        logger.info(
            "cre_cap_rate_aggregator: %d comps, overall_avg=%.3f%%, outliers=%d",
            n, overall_avg * 100, len(outliers)
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("cre_cap_rate_aggregator failed: %s", e)
        _log_lesson(f"cre_cap_rate_aggregator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to the shared lessons log.

    Args:
        message: Description of the error or lesson to record.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError as log_err:
        logger.warning("Could not write to lessons.md: %s", log_err)
