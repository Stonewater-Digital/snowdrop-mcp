"""
Executive Summary: Benchmarks fund performance against vintage-year peer data by computing PME ratio and quartile ranking across TVPI, DPI, and IRR.

Inputs: fund_returns (dict: tvpi float, dpi float, irr float), benchmark_data (dict: median_tvpi, median_dpi, upper_quartile_tvpi, lower_quartile_tvpi)
Outputs: dict with pme_ratio (float), quartile_rank (str), comparison_table (dict)
MCP Tool Name: vintage_year_benchmarking
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "vintage_year_benchmarking",
    "description": (
        "Benchmarks a private equity fund's performance against vintage-year peer data. "
        "Calculates the Public Market Equivalent (PME) ratio as fund_tvpi / benchmark_median_tvpi, "
        "determines quartile rank (Q1=top), and produces a side-by-side comparison table "
        "for TVPI, DPI, and IRR."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_returns": {
                "type": "object",
                "properties": {
                    "tvpi": {"type": "number", "description": "Total Value to Paid-In multiple (e.g. 2.1)"},
                    "dpi": {"type": "number", "description": "Distributions to Paid-In multiple (e.g. 0.8)"},
                    "irr": {"type": "number", "description": "Net IRR as decimal (e.g. 0.185 for 18.5%)"}
                },
                "required": ["tvpi", "dpi", "irr"]
            },
            "benchmark_data": {
                "type": "object",
                "properties": {
                    "median_tvpi": {"type": "number"},
                    "median_dpi": {"type": "number"},
                    "median_irr": {"type": "number"},
                    "upper_quartile_tvpi": {"type": "number", "description": "Q1/Q2 breakpoint (75th percentile)"},
                    "lower_quartile_tvpi": {"type": "number", "description": "Q3/Q4 breakpoint (25th percentile)"}
                },
                "required": ["median_tvpi", "median_dpi", "upper_quartile_tvpi", "lower_quartile_tvpi"]
            }
        },
        "required": ["fund_returns", "benchmark_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "pme_ratio": {"type": "number"},
            "quartile_rank": {"type": "string", "enum": ["Q1", "Q2", "Q3", "Q4"]},
            "comparison_table": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["pme_ratio", "quartile_rank", "comparison_table", "status", "timestamp"]
    }
}


def _quartile_rank(fund_tvpi: float, upper_quartile: float, median: float, lower_quartile: float) -> str:
    """Determine the quartile rank of a fund based on TVPI benchmarks.

    Quartile conventions for private equity (higher TVPI = better):
    - Q1: >= upper_quartile (top 25%)
    - Q2: >= median and < upper_quartile (50th–75th percentile)
    - Q3: >= lower_quartile and < median (25th–50th percentile)
    - Q4: < lower_quartile (bottom 25%)

    Args:
        fund_tvpi: The fund's TVPI multiple.
        upper_quartile: Benchmark upper quartile TVPI (75th percentile).
        median: Benchmark median TVPI (50th percentile).
        lower_quartile: Benchmark lower quartile TVPI (25th percentile).

    Returns:
        Quartile string: 'Q1', 'Q2', 'Q3', or 'Q4'.
    """
    if fund_tvpi >= upper_quartile:
        return "Q1"
    elif fund_tvpi >= median:
        return "Q2"
    elif fund_tvpi >= lower_quartile:
        return "Q3"
    else:
        return "Q4"


def _pct_diff(fund_val: float, benchmark_val: float) -> float | None:
    """Compute percentage difference of fund vs benchmark value.

    Args:
        fund_val: Fund metric value.
        benchmark_val: Benchmark median value.

    Returns:
        Percentage difference as float, or None if benchmark_val is zero.
    """
    if benchmark_val == 0:
        return None
    return round((fund_val - benchmark_val) / benchmark_val * 100, 2)


def vintage_year_benchmarking(**kwargs: Any) -> dict:
    """Compare fund performance to vintage-year benchmarks and assign quartile rank.

    The PME (Public Market Equivalent) ratio here is computed as a simplified
    TVPI-to-benchmark-TVPI ratio. A PME > 1.0 indicates the fund outperforms
    its peer median on an absolute return basis. For cash-flow-based PME
    (KS-PME, Long-Nickels), provide time-series cash flows to a dedicated
    IRR-matching skill.

    Quartile ranking is TVPI-based per standard PE convention (Cambridge Associates,
    Preqin, PitchBook all use TVPI for primary quartiling).

    Args:
        **kwargs: Keyword arguments containing:
            fund_returns (dict): Fund performance with keys:
                - tvpi (float): Total Value to Paid-In multiple
                - dpi (float): Distributions to Paid-In multiple
                - irr (float): Net IRR as decimal (0.185 = 18.5%)
            benchmark_data (dict): Peer benchmark statistics with keys:
                - median_tvpi (float): Peer median TVPI
                - median_dpi (float): Peer median DPI
                - median_irr (float, optional): Peer median net IRR
                - upper_quartile_tvpi (float): 75th percentile TVPI
                - lower_quartile_tvpi (float): 25th percentile TVPI

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - pme_ratio (float): fund_tvpi / median_tvpi
                - quartile_rank (str): 'Q1' through 'Q4'
                - comparison_table (dict): Side-by-side fund vs benchmark metrics
                - outperformance_summary (str): Human-readable summary
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        fund_returns: dict = kwargs.get("fund_returns", {})
        benchmark_data: dict = kwargs.get("benchmark_data", {})

        if not fund_returns:
            raise ValueError("fund_returns is required and cannot be empty")
        if not benchmark_data:
            raise ValueError("benchmark_data is required and cannot be empty")

        fund_tvpi = float(fund_returns["tvpi"])
        fund_dpi = float(fund_returns["dpi"])
        fund_irr = float(fund_returns["irr"])

        median_tvpi = float(benchmark_data["median_tvpi"])
        median_dpi = float(benchmark_data["median_dpi"])
        median_irr = float(benchmark_data.get("median_irr", 0)) if benchmark_data.get("median_irr") is not None else None
        upper_quartile_tvpi = float(benchmark_data["upper_quartile_tvpi"])
        lower_quartile_tvpi = float(benchmark_data["lower_quartile_tvpi"])

        if median_tvpi <= 0:
            raise ValueError(f"median_tvpi must be positive, got {median_tvpi}")
        if upper_quartile_tvpi < median_tvpi:
            raise ValueError(
                f"upper_quartile_tvpi ({upper_quartile_tvpi}) cannot be less than "
                f"median_tvpi ({median_tvpi})"
            )
        if lower_quartile_tvpi > median_tvpi:
            raise ValueError(
                f"lower_quartile_tvpi ({lower_quartile_tvpi}) cannot exceed "
                f"median_tvpi ({median_tvpi})"
            )

        pme_ratio = round(fund_tvpi / median_tvpi, 4)
        quartile = _quartile_rank(fund_tvpi, upper_quartile_tvpi, median_tvpi, lower_quartile_tvpi)

        tvpi_diff = _pct_diff(fund_tvpi, median_tvpi)
        dpi_diff = _pct_diff(fund_dpi, median_dpi)
        irr_diff = _pct_diff(fund_irr, median_irr) if median_irr else None

        comparison_table = {
            "tvpi": {
                "fund": fund_tvpi,
                "benchmark_median": median_tvpi,
                "benchmark_upper_quartile": upper_quartile_tvpi,
                "benchmark_lower_quartile": lower_quartile_tvpi,
                "vs_median_pct": tvpi_diff,
            },
            "dpi": {
                "fund": fund_dpi,
                "benchmark_median": median_dpi,
                "vs_median_pct": dpi_diff,
            },
            "irr": {
                "fund": round(fund_irr * 100, 2),
                "fund_raw": fund_irr,
                "benchmark_median_pct": round(median_irr * 100, 2) if median_irr is not None else None,
                "vs_median_pct": irr_diff,
            },
        }

        pme_label = "outperforms" if pme_ratio > 1.0 else "underperforms"
        outperformance_summary = (
            f"Fund {pme_label} vintage-year peer median on TVPI basis "
            f"(PME: {pme_ratio:.2f}x). Quartile rank: {quartile}. "
            f"TVPI {fund_tvpi:.2f}x vs median {median_tvpi:.2f}x "
            f"({'+' if tvpi_diff and tvpi_diff > 0 else ''}{tvpi_diff:.1f}%)."
        )

        result = {
            "pme_ratio": pme_ratio,
            "quartile_rank": quartile,
            "comparison_table": comparison_table,
            "outperformance_summary": outperformance_summary,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"vintage_year_benchmarking failed: {e}")
        _log_lesson(f"vintage_year_benchmarking: {e}")
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
