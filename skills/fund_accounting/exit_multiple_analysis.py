"""
Executive Summary: Analyzes realized exits by computing MoIC multiples per investment and aggregating statistics by sector and exit type.

Inputs: exits (list[dict]: company, sector, entry_year, exit_year, entry_valuation, exit_valuation, exit_type)
Outputs: dict with exits_with_multiples (list), median_multiple (float), mean_multiple (float), by_sector (dict), by_exit_type (dict)
MCP Tool Name: exit_multiple_analysis
"""
import os
import logging
import statistics
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "exit_multiple_analysis",
    "description": (
        "Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) "
        "multiples for each position. Aggregates median, mean, min, and max multiples at the "
        "portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "exits": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string"},
                        "sector": {"type": "string"},
                        "entry_year": {"type": "integer"},
                        "exit_year": {"type": "integer"},
                        "entry_valuation": {"type": "number", "description": "Cost basis / invested capital ($)"},
                        "exit_valuation": {"type": "number", "description": "Gross proceeds at exit ($)"},
                        "exit_type": {
                            "type": "string",
                            "description": "e.g. 'IPO', 'M&A', 'secondary', 'write-off', 'recap'"
                        }
                    },
                    "required": ["company", "sector", "entry_year", "exit_year",
                                 "entry_valuation", "exit_valuation", "exit_type"]
                },
                "minItems": 1
            }
        },
        "required": ["exits"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "exits_with_multiples": {"type": "array"},
            "median_multiple": {"type": "number"},
            "mean_multiple": {"type": "number"},
            "min_multiple": {"type": "number"},
            "max_multiple": {"type": "number"},
            "by_sector": {"type": "object"},
            "by_exit_type": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": [
            "exits_with_multiples", "median_multiple", "mean_multiple",
            "by_sector", "by_exit_type", "status", "timestamp"
        ]
    }
}


def _moic(exit_valuation: float, entry_valuation: float) -> float:
    """Compute MoIC (Money-on-Invested-Capital) multiple.

    Args:
        exit_valuation: Gross proceeds received at exit.
        entry_valuation: Capital invested (cost basis).

    Returns:
        MoIC multiple rounded to 4 decimal places.

    Raises:
        ZeroDivisionError: If entry_valuation is zero.
    """
    if entry_valuation == 0:
        raise ZeroDivisionError("entry_valuation is zero — cannot compute MoIC")
    return round(exit_valuation / entry_valuation, 4)


def _holding_period_years(entry_year: int, exit_year: int) -> float:
    """Compute approximate holding period in years.

    Args:
        entry_year: Year of initial investment.
        exit_year: Year of exit.

    Returns:
        Holding period as float years.
    """
    return float(exit_year - entry_year)


def _aggregate_group_stats(multiples: list[float], capital_invested: list[float]) -> dict:
    """Compute grouped statistics for a set of exit multiples.

    Args:
        multiples: List of MoIC multiples for the group.
        capital_invested: Parallel list of entry valuations for weighted avg.

    Returns:
        Dict with median, mean, min, max, count, weighted_avg_multiple, and
        total_capital_invested.
    """
    if not multiples:
        return {}

    total_invested = sum(capital_invested)
    if total_invested > 0:
        weighted_avg = round(
            sum(m * c for m, c in zip(multiples, capital_invested)) / total_invested, 4
        )
    else:
        weighted_avg = None

    return {
        "count": len(multiples),
        "median_multiple": round(statistics.median(multiples), 4),
        "mean_multiple": round(statistics.mean(multiples), 4),
        "min_multiple": round(min(multiples), 4),
        "max_multiple": round(max(multiples), 4),
        "weighted_avg_multiple": weighted_avg,
        "total_capital_invested": round(total_invested, 2),
        "stdev_multiple": round(statistics.stdev(multiples), 4) if len(multiples) > 1 else None,
    }


def exit_multiple_analysis(**kwargs: Any) -> dict:
    """Analyze realized exits and produce MoIC statistics at portfolio and group levels.

    Computes MoIC = exit_valuation / entry_valuation for each exit.
    Portfolio-level stats use simple median/mean. Group-level stats also provide
    capital-weighted average to better reflect dollar-weighted outcomes.

    Write-offs (exit_valuation = 0) produce MoIC of 0.0x and are included in
    all statistics to accurately represent loss ratios.

    Args:
        **kwargs: Keyword arguments containing:
            exits (list[dict]): Each dict must have:
                - company (str): Portfolio company name
                - sector (str): Industry sector label
                - entry_year (int): Year of initial investment
                - exit_year (int): Year of exit
                - entry_valuation (float): Invested capital / cost basis
                - exit_valuation (float): Gross proceeds at exit
                - exit_type (str): 'IPO' | 'M&A' | 'secondary' | 'write-off' | 'recap' | other

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - exits_with_multiples (list[dict]): Each exit enriched with moic, holding_years
                - median_multiple (float): Portfolio median MoIC
                - mean_multiple (float): Portfolio mean MoIC
                - min_multiple (float): Lowest MoIC in portfolio
                - max_multiple (float): Highest MoIC in portfolio
                - by_sector (dict): Sector-level aggregated stats
                - by_exit_type (dict): Exit-type-level aggregated stats
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        exits: list[dict] = kwargs.get("exits", [])

        if not exits:
            raise ValueError("exits list is empty — at least one exit is required")

        exits_with_multiples: list[dict] = []
        all_multiples: list[float] = []
        all_invested: list[float] = []

        sector_multiples: dict[str, list[float]] = {}
        sector_invested: dict[str, list[float]] = {}
        exit_type_multiples: dict[str, list[float]] = {}
        exit_type_invested: dict[str, list[float]] = {}

        for ex in exits:
            company: str = ex["company"]
            sector: str = ex.get("sector", "Unknown")
            entry_year: int = int(ex["entry_year"])
            exit_year: int = int(ex["exit_year"])
            entry_val: float = float(ex["entry_valuation"])
            exit_val: float = float(ex["exit_valuation"])
            exit_type: str = ex.get("exit_type", "unknown")

            if entry_val < 0:
                raise ValueError(f"Company '{company}': entry_valuation cannot be negative ({entry_val})")
            if exit_val < 0:
                raise ValueError(f"Company '{company}': exit_valuation cannot be negative ({exit_val})")
            if exit_year < entry_year:
                raise ValueError(
                    f"Company '{company}': exit_year ({exit_year}) is before entry_year ({entry_year})"
                )

            moic = _moic(exit_val, entry_val) if entry_val > 0 else 0.0
            holding_years = _holding_period_years(entry_year, exit_year)

            # Simple annualized return (CAGR) — undefined for 0-year holds
            if holding_years > 0 and moic > 0:
                cagr = round((moic ** (1.0 / holding_years)) - 1.0, 6)
            else:
                cagr = None

            enriched = {
                "company": company,
                "sector": sector,
                "entry_year": entry_year,
                "exit_year": exit_year,
                "entry_valuation": entry_val,
                "exit_valuation": exit_val,
                "exit_type": exit_type,
                "moic": moic,
                "holding_years": holding_years,
                "gross_profit": round(exit_val - entry_val, 2),
                "cagr": cagr,
            }
            exits_with_multiples.append(enriched)
            all_multiples.append(moic)
            all_invested.append(entry_val)

            sector_multiples.setdefault(sector, []).append(moic)
            sector_invested.setdefault(sector, []).append(entry_val)
            exit_type_multiples.setdefault(exit_type, []).append(moic)
            exit_type_invested.setdefault(exit_type, []).append(entry_val)

        # Sort exits by MoIC descending (best performers first)
        exits_with_multiples.sort(key=lambda x: x["moic"], reverse=True)

        portfolio_median = round(statistics.median(all_multiples), 4)
        portfolio_mean = round(statistics.mean(all_multiples), 4)
        portfolio_min = round(min(all_multiples), 4)
        portfolio_max = round(max(all_multiples), 4)
        portfolio_stdev = round(statistics.stdev(all_multiples), 4) if len(all_multiples) > 1 else None

        by_sector = {
            sector: _aggregate_group_stats(mults, sector_invested[sector])
            for sector, mults in sector_multiples.items()
        }
        by_exit_type = {
            et: _aggregate_group_stats(mults, exit_type_invested[et])
            for et, mults in exit_type_multiples.items()
        }

        result = {
            "exits_with_multiples": exits_with_multiples,
            "n_exits": len(exits_with_multiples),
            "median_multiple": portfolio_median,
            "mean_multiple": portfolio_mean,
            "min_multiple": portfolio_min,
            "max_multiple": portfolio_max,
            "stdev_multiple": portfolio_stdev,
            "total_capital_invested": round(sum(all_invested), 2),
            "by_sector": by_sector,
            "by_exit_type": by_exit_type,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"exit_multiple_analysis failed: {e}")
        _log_lesson(f"exit_multiple_analysis: {e}")
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
