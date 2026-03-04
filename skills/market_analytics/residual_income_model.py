"""
Execuve Summary: Values equity using the Residual Income Model (RIM).
Inputs: book_value (float), roe (float), cost_of_equity (float), years (int), terminal_roe (float)
Outputs: intrinsic_value (float), residual_income_per_year (list[float]), terminal_value (float), value_vs_book (float)
MCP Tool Name: residual_income_model
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "residual_income_model",
    "description": "Discounts residual incomes plus current book value to estimate intrinsic value.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "book_value": {"type": "number", "description": "Current book value per share."},
            "roe": {"type": "number", "description": "Return on equity in stage 1 (decimal)."},
            "cost_of_equity": {"type": "number", "description": "Required return (decimal)."},
            "years": {"type": "integer", "description": "Explicit forecast years."},
            "terminal_roe": {"type": "number", "description": "ROE applied to terminal period."}
        },
        "required": ["book_value", "roe", "cost_of_equity", "years", "terminal_roe"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def residual_income_model(**kwargs: Any) -> dict:
    """Calculates intrinsic value using RIM and a terminal value assumption."""
    try:
        book = kwargs.get("book_value")
        roe = kwargs.get("roe")
        cost = kwargs.get("cost_of_equity")
        years = kwargs.get("years")
        terminal_roe = kwargs.get("terminal_roe")
        for label, value in (("book_value", book), ("roe", roe), ("cost_of_equity", cost), ("terminal_roe", terminal_roe)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if not isinstance(years, int) or years <= 0:
            raise ValueError("years must be positive integer")

        residuals = []
        pv_residuals = 0.0
        current_book = book
        for year in range(1, years + 1):
            income = current_book * roe
            residual_income = income - cost * current_book
            residuals.append(residual_income)
            pv_residuals += residual_income / ((1 + cost) ** year)
            current_book = current_book * (1 + roe)
        terminal_income = current_book * terminal_roe
        terminal_residual = terminal_income - cost * current_book
        terminal_value = terminal_residual / (cost * (1 + cost) ** years) if cost != 0 else math.inf
        intrinsic_value = book + pv_residuals + terminal_value
        value_vs_book = intrinsic_value / book if book else math.inf

        return {
            "status": "success",
            "data": {
                "intrinsic_value": intrinsic_value,
                "residual_income_per_year": residuals,
                "terminal_value": terminal_value,
                "value_vs_book": value_vs_book
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"residual_income_model failed: {e}")
        _log_lesson(f"residual_income_model: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
