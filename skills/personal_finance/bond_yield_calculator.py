"""
Executive Smary: Approximates bond current yield, YTM, YTC, and duration for pricing decisions.
Inputs: face_value (float), coupon_rate (float), purchase_price (float), years_to_maturity (float), call_price (float), years_to_call (float)
Outputs: current_yield (float), ytm (float), ytc (float|None), duration_approx (float)
MCP Tool Name: bond_yield_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "bond_yield_calculator",
    "description": (
        "Provides quick estimates for a bond's current yield, yield to maturity, yield to "
        "call, and duration approximation from price and coupon inputs."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "face_value": {
                "type": "number",
                "description": "Principal amount payable at maturity.",
            },
            "coupon_rate": {
                "type": "number",
                "description": "Annual coupon rate as decimal.",
            },
            "purchase_price": {
                "type": "number",
                "description": "Clean price paid for the bond.",
            },
            "years_to_maturity": {
                "type": "number",
                "description": "Years remaining until maturity date.",
            },
            "call_price": {
                "type": "number",
                "description": "Optional call price if the bond is callable.",
            },
            "years_to_call": {
                "type": "number",
                "description": "Optional years until first call date.",
            },
        },
        "required": ["face_value", "coupon_rate", "purchase_price", "years_to_maturity"],
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


def bond_yield_calculator(**kwargs: Any) -> dict:
    """Estimate bond yields and a simple duration metric."""
    try:
        face_value = float(kwargs["face_value"])
        coupon_rate = float(kwargs["coupon_rate"])
        purchase_price = float(kwargs["purchase_price"])
        years_to_maturity = float(kwargs["years_to_maturity"])
        call_price = kwargs.get("call_price")
        years_to_call = kwargs.get("years_to_call")

        if face_value <= 0 or purchase_price <= 0 or years_to_maturity <= 0:
            raise ValueError("face_value, purchase_price, and years_to_maturity must be positive")

        annual_coupon = face_value * coupon_rate
        current_yield = annual_coupon / purchase_price
        ytm = (
            (annual_coupon + (face_value - purchase_price) / years_to_maturity)
            / ((face_value + purchase_price) / 2)
        )

        ytc: Optional[float] = None
        if call_price is not None and years_to_call:
            call_price_f = float(call_price)
            years_to_call_f = float(years_to_call)
            if years_to_call_f > 0:
                ytc = (
                    (annual_coupon + (call_price_f - purchase_price) / years_to_call_f)
                    / ((call_price_f + purchase_price) / 2)
                )

        duration_approx = years_to_maturity / (1 + ytm) if ytm > 0 else years_to_maturity

        return {
            "status": "success",
            "data": {
                "current_yield": current_yield,
                "ytm": ytm,
                "ytc": ytc,
                "duration_approx": duration_approx,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"bond_yield_calculator failed: {e}")
        _log_lesson(f"bond_yield_calculator: {e}")
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
