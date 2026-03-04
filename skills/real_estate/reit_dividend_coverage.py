"""
Executive Summary: Evaluates REIT dividend sustainability by comparing FFO and AFFO payout coverage ratios.
Inputs: ffo (float), dividends_paid (float), affo (float, optional)
Outputs: dict with coverage_ratio (float), affo_coverage (float or null), sustainable (bool), risk_level (str)
MCP Tool Name: reit_dividend_coverage
"""
import os
import logging
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "reit_dividend_coverage",
    "description": (
        "Evaluates REIT dividend sustainability by computing FFO and AFFO payout "
        "coverage ratios. Classifies risk as low, medium, or high, and flags "
        "dividends at risk of cuts."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "ffo": {
                "type": "number",
                "description": "Funds From Operations for the period (dollars)."
            },
            "dividends_paid": {
                "type": "number",
                "description": "Total dividends paid to shareholders for the period (dollars)."
            },
            "affo": {
                "type": "number",
                "description": "Adjusted FFO for the period (optional, dollars)."
            }
        },
        "required": ["ffo", "dividends_paid"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "coverage_ratio":  {"type": "number"},
                    "affo_coverage":   {"type": ["number", "null"]},
                    "sustainable":     {"type": "boolean"},
                    "risk_level":      {"type": "string"},
                    "payout_ratio_pct": {"type": "number"},
                    "commentary":      {"type": "string"}
                },
                "required": ["coverage_ratio", "sustainable", "risk_level"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Coverage ratio thresholds (FFO / Dividends)
LOW_RISK_THRESHOLD: float = 1.20    # >120% coverage = low risk
MEDIUM_RISK_THRESHOLD: float = 1.00  # 100–120% coverage = medium risk
# Below 1.0 = high risk / unsustainable


def reit_dividend_coverage(
    ffo: float,
    dividends_paid: float,
    affo: Optional[float] = None,
    **kwargs: Any
) -> dict:
    """Compute REIT dividend coverage ratios and sustainability classification.

    Coverage Ratio = FFO / Dividends Paid. A ratio below 1.0 indicates dividends
    exceed earnings and are likely unsustainable. AFFO coverage is computed when
    AFFO is provided (AFFO is a stricter test as it deducts maintenance CapEx).

    Risk Classification:
      - Low:    Coverage >= 1.20
      - Medium: Coverage >= 1.00 and < 1.20
      - High:   Coverage < 1.00

    Args:
        ffo: Funds From Operations for the period.
        dividends_paid: Total dividends distributed to shareholders.
        affo: Adjusted FFO (optional). Used for stricter coverage test.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (coverage_ratio, affo_coverage, sustainable,
        risk_level, payout_ratio_pct, commentary), timestamp.

    Raises:
        ValueError: If dividends_paid is zero or negative.
    """
    try:
        ffo = float(ffo)
        dividends_paid = float(dividends_paid)

        if dividends_paid <= 0:
            raise ValueError(f"dividends_paid must be positive, got {dividends_paid}")

        # FFO-based coverage
        coverage_ratio: float = round(ffo / dividends_paid, 4)
        payout_ratio_pct: float = round((dividends_paid / ffo * 100), 2) if ffo > 0 else float("inf")

        # AFFO-based coverage (stricter)
        affo_coverage: Optional[float] = None
        if affo is not None:
            affo = float(affo)
            affo_coverage = round(affo / dividends_paid, 4)

        # Sustainability determination (use AFFO if available, else FFO)
        primary_coverage = affo_coverage if affo_coverage is not None else coverage_ratio
        sustainable: bool = primary_coverage >= MEDIUM_RISK_THRESHOLD

        # Risk level
        if primary_coverage >= LOW_RISK_THRESHOLD:
            risk_level = "low"
            commentary = (
                f"Coverage of {primary_coverage:.2f}x is healthy. "
                "Dividend is well-supported with room for future increases."
            )
        elif primary_coverage >= MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
            commentary = (
                f"Coverage of {primary_coverage:.2f}x is adequate but thin. "
                "Any FFO decline would quickly put the dividend at risk. Monitor closely."
            )
        else:
            risk_level = "high"
            sustainable = False
            commentary = (
                f"Coverage of {primary_coverage:.2f}x is below 1.0 — "
                "dividends exceed {'AFFO' if affo_coverage is not None else 'FFO'}. "
                "Dividend cut or share issuance to fund distribution is likely."
            )

        # Additional flag: FFO negative
        if ffo < 0:
            risk_level = "high"
            sustainable = False
            commentary = "FFO is negative — dividend is entirely unsustainable."

        result: dict = {
            "ffo": ffo,
            "dividends_paid": dividends_paid,
            "coverage_ratio": coverage_ratio,
            "payout_ratio_pct": payout_ratio_pct,
            "sustainable": sustainable,
            "risk_level": risk_level,
            "commentary": commentary
        }

        if affo_coverage is not None:
            result["affo"] = affo
            result["affo_coverage"] = affo_coverage
            result["affo_payout_ratio_pct"] = round((dividends_paid / affo * 100), 2) if affo and affo > 0 else None
        else:
            result["affo_coverage"] = None

        logger.info(
            "reit_dividend_coverage: coverage=%.4f, risk=%s, sustainable=%s",
            coverage_ratio, risk_level, sustainable
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("reit_dividend_coverage failed: %s", e)
        _log_lesson(f"reit_dividend_coverage: {e}")
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
