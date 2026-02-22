"""
Executive Summary: Calculates available dry powder, deployment rate, and optional deployment runway from fund commitment and call data.

Inputs: total_commitments (float), capital_called (float), reserves (float), monthly_deployment_rate (float, optional)
Outputs: dict with dry_powder (float), deployment_rate_pct (float), runway_months (float | None), reserves (float)
MCP Tool Name: dry_powder_calculator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dry_powder_calculator",
    "description": (
        "Calculates available dry powder (uninvested capital), deployment rate, "
        "and deployment runway for a private equity fund. "
        "Dry powder = total_commitments - capital_called - reserves. "
        "If monthly_deployment_rate is provided, runway_months = dry_powder / rate. "
        "Useful for fund pacing, LP reporting, and GP investment planning."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_commitments": {
                "type": "number",
                "description": "Total LP capital committed to the fund ($)"
            },
            "capital_called": {
                "type": "number",
                "description": "Total capital drawn down from LPs to date ($)"
            },
            "reserves": {
                "type": "number",
                "description": "Capital earmarked / reserved for follow-ons and fees ($)"
            },
            "monthly_deployment_rate": {
                "type": "number",
                "description": "Average monthly deployment in dollars (optional — enables runway calculation)"
            }
        },
        "required": ["total_commitments", "capital_called", "reserves"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "dry_powder": {"type": "number"},
            "deployment_rate_pct": {"type": "number"},
            "runway_months": {"type": ["number", "null"]},
            "reserves": {"type": "number"},
            "uncalled_capital": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["dry_powder", "deployment_rate_pct", "runway_months", "reserves", "status", "timestamp"]
    }
}


def dry_powder_calculator(**kwargs: Any) -> dict:
    """Calculate dry powder, deployment velocity, and runway for a PE fund.

    Key definitions:
    - uncalled_capital: LP commitments not yet drawn (total_commitments - capital_called)
    - reserves: Earmarked portion of uncalled capital (follow-on, fees, recycling)
    - dry_powder: Freely deployable capital (uncalled_capital - reserves)
    - deployment_rate: Fraction of total commitments already drawn (capital_called / total_commitments)
    - runway_months: How long dry_powder lasts at current monthly_deployment_rate

    Note: dry_powder can be zero but not negative by design. If reserves exceed
    uncalled capital, dry_powder is clamped to zero and a warning is included.

    Args:
        **kwargs: Keyword arguments containing:
            total_commitments (float): Total fund size (LP commitments).
            capital_called (float): Capital drawn to date.
            reserves (float): Earmarked capital not available for new investments.
            monthly_deployment_rate (float, optional): Avg monthly deployment in $.

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - dry_powder (float): Available uninvested capital
                - deployment_rate_pct (float): % of commitments called
                - runway_months (float | None): Months of dry powder at current pace
                - runway_years (float | None): runway_months / 12
                - reserves (float): Earmarked capital
                - uncalled_capital (float): Not-yet-drawn LP commitments
                - called_pct (float): capital_called / total_commitments * 100
                - remaining_commitment_pct (float): uncalled / total * 100
                - warnings (list[str]): Any anomaly flags
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        total_commitments: float = float(kwargs.get("total_commitments", 0))
        capital_called: float = float(kwargs.get("capital_called", 0))
        reserves: float = float(kwargs.get("reserves", 0))
        monthly_rate_raw = kwargs.get("monthly_deployment_rate")
        monthly_deployment_rate: float | None = float(monthly_rate_raw) if monthly_rate_raw is not None else None

        # Input validation
        if total_commitments <= 0:
            raise ValueError(f"total_commitments must be positive, got {total_commitments}")
        if capital_called < 0:
            raise ValueError(f"capital_called cannot be negative, got {capital_called}")
        if reserves < 0:
            raise ValueError(f"reserves cannot be negative, got {reserves}")
        if capital_called > total_commitments:
            raise ValueError(
                f"capital_called ({capital_called:,.2f}) exceeds total_commitments "
                f"({total_commitments:,.2f}) — check inputs"
            )
        if monthly_deployment_rate is not None and monthly_deployment_rate < 0:
            raise ValueError(f"monthly_deployment_rate cannot be negative, got {monthly_deployment_rate}")

        warnings: list[str] = []

        uncalled_capital = round(total_commitments - capital_called, 6)
        raw_dry_powder = uncalled_capital - reserves

        if raw_dry_powder < 0:
            warnings.append(
                f"Reserves (${reserves:,.2f}) exceed uncalled capital (${uncalled_capital:,.2f}). "
                f"Dry powder clamped to $0. Review reserve methodology."
            )
        dry_powder = max(0.0, round(raw_dry_powder, 6))

        deployment_rate_pct = round(capital_called / total_commitments * 100, 4)
        remaining_commitment_pct = round(uncalled_capital / total_commitments * 100, 4)

        # Runway calculation
        runway_months: float | None = None
        runway_years: float | None = None

        if monthly_deployment_rate is not None:
            if monthly_deployment_rate == 0:
                warnings.append(
                    "monthly_deployment_rate is 0 — runway is undefined (infinite). Returning null."
                )
                runway_months = None
                runway_years = None
            else:
                runway_months = round(dry_powder / monthly_deployment_rate, 4)
                runway_years = round(runway_months / 12, 4)

        # Pace health assessment
        pace_status: str
        if deployment_rate_pct < 25:
            pace_status = "EARLY_STAGE"
        elif deployment_rate_pct < 60:
            pace_status = "MID_DEPLOYMENT"
        elif deployment_rate_pct < 85:
            pace_status = "LATE_STAGE"
        else:
            pace_status = "NEAR_FULLY_DEPLOYED"

        result = {
            "dry_powder": dry_powder,
            "deployment_rate_pct": deployment_rate_pct,
            "runway_months": runway_months,
            "runway_years": runway_years,
            "reserves": reserves,
            "uncalled_capital": uncalled_capital,
            "capital_called": capital_called,
            "total_commitments": total_commitments,
            "called_pct": deployment_rate_pct,
            "remaining_commitment_pct": remaining_commitment_pct,
            "monthly_deployment_rate": monthly_deployment_rate,
            "pace_status": pace_status,
            "warnings": warnings,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"dry_powder_calculator failed: {e}")
        _log_lesson(f"dry_powder_calculator: {e}")
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
