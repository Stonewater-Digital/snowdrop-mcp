"""
Executive Summary: Analyzes sovereign nation reserve composition across fiat, gold, and digital assets against IMF adequacy benchmarks.
Inputs: reserves (dict: fiat_usd float, gold_tonnes float, gold_price_usd float, digital_assets list[dict], sdr_holdings float), imports_monthly (float, optional)
Outputs: total_reserves_usd (float), breakdown_pct (dict), import_coverage_months (float), adequacy_assessment (str)
MCP Tool Name: sovereign_reserves_analyzer
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sovereign_reserves_analyzer",
    "description": "Analyzes sovereign reserve composition (fiat/gold/digital) and compares against IMF adequacy metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "reserves": {
                "type": "object",
                "description": "Reserve holdings breakdown",
                "properties": {
                    "fiat_usd": {"type": "number", "description": "Fiat currency holdings in USD"},
                    "gold_tonnes": {"type": "number", "description": "Gold holdings in metric tonnes"},
                    "gold_price_usd": {"type": "number", "description": "Current gold price per troy ounce USD"},
                    "digital_assets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "asset": {"type": "string"},
                                "amount": {"type": "number"},
                                "price_usd": {"type": "number"}
                            }
                        }
                    },
                    "sdr_holdings": {"type": "number", "description": "SDR holdings (in SDR units)"}
                },
                "required": ["fiat_usd", "gold_tonnes", "gold_price_usd"]
            },
            "imports_monthly": {"type": "number", "description": "Monthly import bill in USD (optional)"},
            "sdr_usd_rate": {"type": "number", "description": "SDR to USD conversion rate (default: 1.33)"}
        },
        "required": ["reserves"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "total_reserves_usd": {"type": "number"},
                    "breakdown_pct": {"type": "object"},
                    "import_coverage_months": {"type": "number"},
                    "adequacy_assessment": {"type": "string"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Troy ounces per metric tonne
TROY_OZ_PER_TONNE = 32_150.7


def sovereign_reserves_analyzer(
    reserves: dict[str, Any],
    imports_monthly: float | None = None,
    sdr_usd_rate: float = 1.33,
    **kwargs: Any
) -> dict[str, Any]:
    """Analyze sovereign reserve composition and IMF adequacy.

    Computes total reserve value, percentage breakdown across asset classes,
    and compares to the IMF's Assessing Reserve Adequacy (ARA) benchmark of
    3 months of import coverage.

    Args:
        reserves: Dictionary containing reserve holdings:
            - fiat_usd (float): Foreign currency holdings in USD equivalent.
            - gold_tonnes (float): Gold held in metric tonnes.
            - gold_price_usd (float): Spot price of gold per troy ounce in USD.
            - digital_assets (list[dict], optional): List of crypto/digital assets,
              each with keys 'asset' (str), 'amount' (float), 'price_usd' (float).
            - sdr_holdings (float, optional): IMF Special Drawing Rights in SDR units.
        imports_monthly: Monthly import expenditure in USD. Required to compute
            import coverage months. Defaults to None.
        sdr_usd_rate: USD value of one SDR. Defaults to 1.33 (approximate 2025 rate).
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Analysis results including total_reserves_usd,
              breakdown_pct, import_coverage_months, adequacy_assessment.
            - timestamp (str): ISO-8601 UTC timestamp.

    Raises:
        ValueError: Raised internally if required reserve fields are missing;
            caught and returned as error envelope.
    """
    try:
        fiat_usd: float = float(reserves.get("fiat_usd", 0.0))
        gold_tonnes: float = float(reserves.get("gold_tonnes", 0.0))
        gold_price_usd: float = float(reserves.get("gold_price_usd", 0.0))
        digital_assets: list[dict] = reserves.get("digital_assets", [])
        sdr_holdings: float = float(reserves.get("sdr_holdings", 0.0))

        if gold_price_usd < 0:
            raise ValueError("gold_price_usd must be non-negative")

        # Gold value: convert tonnes to troy ounces, then multiply by spot price
        gold_value_usd: float = gold_tonnes * TROY_OZ_PER_TONNE * gold_price_usd

        # Digital assets value
        digital_value_usd: float = sum(
            float(a.get("amount", 0)) * float(a.get("price_usd", 0))
            for a in digital_assets
        )

        # SDR value in USD
        sdr_value_usd: float = sdr_holdings * sdr_usd_rate

        total_reserves_usd: float = fiat_usd + gold_value_usd + digital_value_usd + sdr_value_usd

        if total_reserves_usd <= 0:
            raise ValueError("Total reserves must be greater than zero")

        # Percentage breakdown
        breakdown_pct: dict[str, float] = {
            "fiat_pct": round(fiat_usd / total_reserves_usd * 100, 4),
            "gold_pct": round(gold_value_usd / total_reserves_usd * 100, 4),
            "digital_pct": round(digital_value_usd / total_reserves_usd * 100, 4),
            "sdr_pct": round(sdr_value_usd / total_reserves_usd * 100, 4),
        }
        breakdown_pct["fiat_usd"] = round(fiat_usd, 2)
        breakdown_pct["gold_usd"] = round(gold_value_usd, 2)
        breakdown_pct["digital_usd"] = round(digital_value_usd, 2)
        breakdown_pct["sdr_usd"] = round(sdr_value_usd, 2)

        # Digital asset detail
        digital_detail = [
            {
                "asset": a.get("asset", "unknown"),
                "amount": float(a.get("amount", 0)),
                "price_usd": float(a.get("price_usd", 0)),
                "value_usd": round(float(a.get("amount", 0)) * float(a.get("price_usd", 0)), 2),
                "pct_of_total": round(
                    float(a.get("amount", 0)) * float(a.get("price_usd", 0)) / total_reserves_usd * 100, 4
                )
            }
            for a in digital_assets
        ]

        # Import coverage (IMF ARA benchmark: minimum 3 months)
        import_coverage_months: float | None = None
        adequacy_assessment: str = "N/A — imports_monthly not provided"

        if imports_monthly and imports_monthly > 0:
            import_coverage_months = round(total_reserves_usd / imports_monthly, 2)

            if import_coverage_months >= 12:
                adequacy_assessment = "STRONG — Coverage exceeds 12 months (3x IMF benchmark)"
            elif import_coverage_months >= 6:
                adequacy_assessment = "ADEQUATE — Coverage 6–12 months (2x IMF benchmark)"
            elif import_coverage_months >= 3:
                adequacy_assessment = "MINIMUM ADEQUATE — Coverage at IMF 3-month benchmark"
            elif import_coverage_months >= 1.5:
                adequacy_assessment = "VULNERABLE — Coverage below IMF benchmark; vulnerability risk elevated"
            else:
                adequacy_assessment = "CRITICAL — Coverage below 2 months; crisis risk"

        result: dict[str, Any] = {
            "total_reserves_usd": round(total_reserves_usd, 2),
            "breakdown_pct": breakdown_pct,
            "digital_asset_detail": digital_detail,
            "gold_value_usd": round(gold_value_usd, 2),
            "gold_tonnes": gold_tonnes,
            "gold_troy_oz": round(gold_tonnes * TROY_OZ_PER_TONNE, 2),
            "import_coverage_months": import_coverage_months,
            "adequacy_assessment": adequacy_assessment,
            "imf_benchmark_months": 3,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"sovereign_reserves_analyzer failed: {e}")
        _log_lesson(f"sovereign_reserves_analyzer: {e}")
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
