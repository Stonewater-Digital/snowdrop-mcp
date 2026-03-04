"""
Executive Summary: Quantifies CDS-cash basis and decomposes drivers for relative-value trades.
Inputs: cash_spread_bp (float), cds_spread_bp (float), repo_rate_bp (float), funding_rate_bp (float), expected_loss_bp (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: cds_basis_trade_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cds_basis_trade_analyzer",
    "description": (
        "Decomposes the CDS-cash basis into coupon, financing, and default-leg components "
        "using basis trading conventions (Hull, Ch. 24)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_spread_bp": {
                "type": "number",
                "description": "Asset-swap or bond spread in basis points of yield."
            },
            "cds_spread_bp": {
                "type": "number",
                "description": "Quoted CDS running spread in basis points."
            },
            "repo_rate_bp": {
                "type": "number",
                "description": "Term repo rate used to finance the bond, in basis points."
            },
            "funding_rate_bp": {
                "type": "number",
                "description": "Dealer funding curve rate for the same maturity, in basis points."
            },
            "expected_loss_bp": {
                "type": "number",
                "description": "Expected default-loss adjustment expressed in basis points."
            }
        },
        "required": [
            "cash_spread_bp",
            "cds_spread_bp",
            "repo_rate_bp",
            "funding_rate_bp",
            "expected_loss_bp"
        ]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def cds_basis_trade_analyzer(**kwargs: Any) -> dict[str, Any]:
    try:
        cash_spread = float(kwargs["cash_spread_bp"])
        cds_spread = float(kwargs["cds_spread_bp"])
        repo_rate = float(kwargs["repo_rate_bp"])
        funding_rate = float(kwargs["funding_rate_bp"])
        expected_loss = float(kwargs["expected_loss_bp"])

        financing_component = funding_rate - repo_rate
        coupon_mismatch = cash_spread - cds_spread
        clean_basis = coupon_mismatch - financing_component - expected_loss
        gross_basis = cash_spread - cds_spread
        relative_value_score = clean_basis / max(abs(cds_spread), 1e-6)

        data = {
            "gross_basis_bp": gross_basis,
            "clean_basis_bp": clean_basis,
            "financing_component_bp": financing_component,
            "default_leg_component_bp": expected_loss,
            "relative_value_score": relative_value_score,
            "hedge_ratio": cds_spread / max(cash_spread, 1e-6)
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("cds_basis_trade_analyzer failed: %s", e)
        _log_lesson(f"cds_basis_trade_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
