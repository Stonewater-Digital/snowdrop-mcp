"""
Executive Smary: Performs DuPont ROE decomposition into 3-factor and 5-factor components.
Inputs: net_income (float), revenue (float), total_assets (float), total_equity (float), ebt (float), ebit (float), interest_expense (float), tax_rate (float)
Outputs: roe (float), profit_margin (float), asset_turnover (float), equity_multiplier (float), tax_burden (float), interest_burden (float), five_factor_decomposition (dict)
MCP Tool Name: dupont_decomposition
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dupont_decomposition",
    "description": (
        "Breaks down ROE using the classic DuPont formula plus a five-factor variant "
        "that isolates tax burden and interest burden effects."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {"type": "number", "description": "Net income after taxes."},
            "revenue": {"type": "number", "description": "Total revenue."},
            "total_assets": {"type": "number", "description": "Average total assets."},
            "total_equity": {"type": "number", "description": "Average shareholders' equity."},
            "ebt": {"type": "number", "description": "Earnings before tax."},
            "ebit": {"type": "number", "description": "Earnings before interest and tax."},
            "interest_expense": {"type": "number", "description": "Interest expense for the period."},
            "tax_rate": {"type": "number", "description": "Effective tax rate used if ebt=0."},
        },
        "required": [
            "net_income",
            "revenue",
            "total_assets",
            "total_equity",
            "ebt",
            "ebit",
            "interest_expense",
            "tax_rate",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def dupont_decomposition(**kwargs: Any) -> dict:
    """Compute ROE via DuPont method, including five-factor decomposition."""
    try:
        net_income = float(kwargs["net_income"])
        revenue = float(kwargs["revenue"])
        total_assets = float(kwargs["total_assets"])
        total_equity = float(kwargs["total_equity"])
        ebt = float(kwargs["ebt"])
        ebit = float(kwargs["ebit"])
        interest_expense = float(kwargs["interest_expense"])
        tax_rate = float(kwargs["tax_rate"])

        profit_margin = net_income / revenue if revenue else 0.0
        asset_turnover = revenue / total_assets if total_assets else 0.0
        equity_multiplier = total_assets / total_equity if total_equity else float("inf")
        roe = profit_margin * asset_turnover * equity_multiplier

        tax_burden = net_income / ebt if ebt else (1 - tax_rate)
        interest_burden = ebt / ebit if ebit else 1.0
        operating_margin = ebit / revenue if revenue else 0.0

        five_factor = {
            "tax_burden": tax_burden,
            "interest_burden": interest_burden,
            "operating_margin": operating_margin,
            "asset_turnover": asset_turnover,
            "equity_multiplier": equity_multiplier,
            "product": tax_burden * interest_burden * operating_margin * asset_turnover * equity_multiplier,
        }

        return {
            "status": "success",
            "data": {
                "roe": roe,
                "profit_margin": profit_margin,
                "asset_turnover": asset_turnover,
                "equity_multiplier": equity_multiplier,
                "tax_burden": tax_burden,
                "interest_burden": interest_burden,
                "five_factor_decomposition": five_factor,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"dupont_decomposition failed: {e}")
        _log_lesson(f"dupont_decomposition: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
