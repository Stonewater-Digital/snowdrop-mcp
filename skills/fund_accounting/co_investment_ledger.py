"""
Executive Summary: Builds a side-by-side co-investment ledger tracking main fund and co-investor exposure per deal with aggregate totals.

Inputs: main_fund_id (str), co_invest_deals (list[dict]: deal_name, main_fund_amount, co_invest_amount, co_investor_names list[str], date str)
Outputs: dict with deals_table (list[dict]), total_main_fund_exposure (float), total_co_invest_exposure (float), total_combined (float)
MCP Tool Name: co_investment_ledger
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "co_investment_ledger",
    "description": (
        "Constructs a co-investment ledger for a private equity fund, showing "
        "main fund capital alongside co-investor capital for each deal. "
        "Calculates total combined exposure per deal, percentage ownership split, "
        "and aggregate exposure totals across the portfolio."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "main_fund_id": {
                "type": "string",
                "description": "Identifier for the main fund (e.g. 'Snowdrop Capital Fund II')"
            },
            "co_invest_deals": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "deal_name": {"type": "string"},
                        "main_fund_amount": {"type": "number", "description": "Main fund capital deployed ($)"},
                        "co_invest_amount": {"type": "number", "description": "Total co-investor capital deployed ($)"},
                        "co_investor_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of co-investor entity names"
                        },
                        "date": {"type": "string", "description": "Investment date in YYYY-MM-DD format"}
                    },
                    "required": ["deal_name", "main_fund_amount", "co_invest_amount", "co_investor_names", "date"]
                },
                "minItems": 1
            }
        },
        "required": ["main_fund_id", "co_invest_deals"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "deals_table": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "deal_name": {"type": "string"},
                        "date": {"type": "string"},
                        "main_fund_amount": {"type": "number"},
                        "co_invest_amount": {"type": "number"},
                        "total_deal_exposure": {"type": "number"},
                        "main_fund_pct": {"type": "number"},
                        "co_invest_pct": {"type": "number"},
                        "co_investor_names": {"type": "array", "items": {"type": "string"}},
                        "n_co_investors": {"type": "integer"}
                    }
                }
            },
            "total_main_fund_exposure": {"type": "number"},
            "total_co_invest_exposure": {"type": "number"},
            "total_combined": {"type": "number"},
            "main_fund_portfolio_pct": {"type": "number"},
            "co_invest_portfolio_pct": {"type": "number"},
            "n_deals": {"type": "integer"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": [
            "deals_table", "total_main_fund_exposure", "total_co_invest_exposure",
            "total_combined", "status", "timestamp"
        ]
    }
}


def co_investment_ledger(**kwargs: Any) -> dict:
    """Build a co-investment ledger with per-deal exposure and aggregate portfolio totals.

    For each deal, computes the total combined investment (main fund + co-investors)
    and calculates what percentage each capital source contributes. At the portfolio
    level, reports aggregate exposure and the overall capital source split.

    Args:
        **kwargs: Keyword arguments containing:
            main_fund_id (str): Name/ID of the main PE fund.
            co_invest_deals (list[dict]): Each dict must have:
                - deal_name (str): Company or deal identifier
                - main_fund_amount (float): Dollars committed by main fund
                - co_invest_amount (float): Total dollars from all co-investors combined
                - co_investor_names (list[str]): Individual co-investor names
                - date (str): Investment date (YYYY-MM-DD)

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - main_fund_id (str): The main fund identifier
                - deals_table (list[dict]): Per-deal ledger rows
                - total_main_fund_exposure (float): Sum of main fund capital
                - total_co_invest_exposure (float): Sum of co-investor capital
                - total_combined (float): Grand total across all deals
                - main_fund_portfolio_pct (float): Main fund share of total portfolio
                - co_invest_portfolio_pct (float): Co-investor share of total portfolio
                - n_deals (int): Number of deals
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        main_fund_id: str = kwargs.get("main_fund_id", "")
        deals_input: list[dict] = kwargs.get("co_invest_deals", [])

        if not main_fund_id or not main_fund_id.strip():
            raise ValueError("main_fund_id is required and cannot be empty")
        if not deals_input:
            raise ValueError("co_invest_deals is empty — at least one deal is required")

        deals_table: list[dict] = []
        total_main = 0.0
        total_co = 0.0

        for deal in deals_input:
            deal_name: str = deal["deal_name"]
            main_amt: float = float(deal["main_fund_amount"])
            co_amt: float = float(deal["co_invest_amount"])
            co_investors: list[str] = deal.get("co_investor_names", [])
            date_str: str = deal.get("date", "")

            if main_amt < 0:
                raise ValueError(f"Deal '{deal_name}': main_fund_amount cannot be negative ({main_amt})")
            if co_amt < 0:
                raise ValueError(f"Deal '{deal_name}': co_invest_amount cannot be negative ({co_amt})")

            total_deal = main_amt + co_amt

            if total_deal > 0:
                main_pct = round(main_amt / total_deal * 100, 4)
                co_pct = round(co_amt / total_deal * 100, 4)
            else:
                main_pct = 0.0
                co_pct = 0.0

            total_main += main_amt
            total_co += co_amt

            deals_table.append({
                "deal_name": deal_name,
                "date": date_str,
                "main_fund_amount": main_amt,
                "co_invest_amount": co_amt,
                "total_deal_exposure": round(total_deal, 4),
                "main_fund_pct": main_pct,
                "co_invest_pct": co_pct,
                "co_investor_names": co_investors,
                "n_co_investors": len(co_investors),
            })

        # Sort by date descending (most recent first), handle missing dates gracefully
        deals_table.sort(key=lambda d: d["date"] or "0000-00-00", reverse=True)

        total_combined = total_main + total_co

        if total_combined > 0:
            main_portfolio_pct = round(total_main / total_combined * 100, 4)
            co_portfolio_pct = round(total_co / total_combined * 100, 4)
        else:
            main_portfolio_pct = 0.0
            co_portfolio_pct = 0.0

        result = {
            "main_fund_id": main_fund_id,
            "deals_table": deals_table,
            "total_main_fund_exposure": round(total_main, 4),
            "total_co_invest_exposure": round(total_co, 4),
            "total_combined": round(total_combined, 4),
            "main_fund_portfolio_pct": main_portfolio_pct,
            "co_invest_portfolio_pct": co_portfolio_pct,
            "n_deals": len(deals_table),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"co_investment_ledger failed: {e}")
        _log_lesson(f"co_investment_ledger: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the shared lessons log.

    Args:
        message: The lesson or error description to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
