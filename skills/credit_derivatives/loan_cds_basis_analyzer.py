"""
Executive Summary: Measures LCDS versus cash loan spread basis with funding and liquidity adjustments.
Inputs: loan_spread_bp (float), lcds_spread_bp (float), funding_basis_bp (float), recovery_rate (float), maturity_years (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: loan_cds_basis_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "loan_cds_basis_analyzer",
    "description": "Decomposes LCDS-cash loan basis into funding, liquidity, and recovery adjustments for basis trades.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "loan_spread_bp": {
                "type": "number",
                "description": "Observed leveraged loan spread (L+bp)."
            },
            "lcds_spread_bp": {
                "type": "number",
                "description": "Quoted LCDS spread for the same borrower in basis points."
            },
            "funding_basis_bp": {
                "type": "number",
                "description": "Liquidity or funding discount to LIBOR/EURIBOR in basis points."
            },
            "recovery_rate": {
                "type": "number",
                "description": "Assumed recovery for secured loans (0-1)."
            },
            "maturity_years": {
                "type": "number",
                "description": "Remaining maturity used for PV01 conversion."
            }
        },
        "required": [
            "loan_spread_bp",
            "lcds_spread_bp",
            "funding_basis_bp",
            "recovery_rate",
            "maturity_years"
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


def loan_cds_basis_analyzer(**kwargs: Any) -> dict[str, Any]:
    try:
        loan_spread = float(kwargs["loan_spread_bp"])
        lcds_spread = float(kwargs["lcds_spread_bp"])
        funding_basis = float(kwargs["funding_basis_bp"])
        recovery = float(kwargs["recovery_rate"])
        maturity = float(kwargs["maturity_years"])
        if maturity <= 0:
            raise ValueError("maturity_years must be positive")
        if not 0.0 <= recovery < 1.0:
            raise ValueError("recovery_rate must be in [0,1)")

        quoted_basis = loan_spread - lcds_spread
        liquidity_component = funding_basis
        recovery_component = (1 - recovery) * 100.0
        clean_basis = quoted_basis - liquidity_component - recovery_component
        pv01 = maturity / 4.0
        pnl_per_10m = clean_basis / 10000.0 * 10_000_000 * pv01

        data = {
            "quoted_basis_bp": quoted_basis,
            "clean_basis_bp": clean_basis,
            "liquidity_component_bp": liquidity_component,
            "recovery_component_bp": recovery_component,
            "pv01_years": pv01,
            "pnl_per_10mm": pnl_per_10m
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("loan_cds_basis_analyzer failed: %s", e)
        _log_lesson(f"loan_cds_basis_analyzer: {e}")
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
