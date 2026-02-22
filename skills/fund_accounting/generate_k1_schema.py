"""
Executive Summary: Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items.

Inputs: partner_id (str), fund_id (str), tax_year (int), allocations (dict)
Outputs: dict with k1_json (partner_info, fund_info, allocations, line_items)
MCP Tool Name: generate_k1_schema
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "generate_k1_schema",
    "description": "Structures partner tax allocation data into an IRS-compatible Schedule K-1 JSON schema with Part III line items.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "partner_id": {"type": "string", "description": "Unique partner identifier"},
            "fund_id": {"type": "string", "description": "Fund entity identifier (EIN or internal ID)"},
            "tax_year": {"type": "integer", "description": "Tax year (e.g. 2025)"},
            "allocations": {
                "type": "object",
                "description": "Partner tax allocations",
                "properties": {
                    "ordinary_income": {"type": "number"},
                    "capital_gains_short": {"type": "number"},
                    "capital_gains_long": {"type": "number"},
                    "tax_exempt_income": {"type": "number"},
                    "deductions": {"type": "number"},
                    "credits": {"type": "number"},
                },
                "required": [
                    "ordinary_income",
                    "capital_gains_short",
                    "capital_gains_long",
                    "tax_exempt_income",
                    "deductions",
                    "credits",
                ],
            },
        },
        "required": ["partner_id", "fund_id", "tax_year", "allocations"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "k1_json": {
                "type": "object",
                "properties": {
                    "partner_info": {"type": "object"},
                    "fund_info": {"type": "object"},
                    "allocations": {"type": "object"},
                    "line_items": {"type": "array"},
                },
            },
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["k1_json", "status", "timestamp"],
    },
}

# IRS Schedule K-1 (Form 1065) Part III line mappings
_K1_LINE_MAP: list[dict] = [
    {"line": "1",  "label": "Ordinary business income (loss)",         "key": "ordinary_income"},
    {"line": "2",  "label": "Net rental real estate income (loss)",     "key": None},
    {"line": "3",  "label": "Other net rental income (loss)",           "key": None},
    {"line": "4",  "label": "Guaranteed payments for services",         "key": None},
    {"line": "5",  "label": "Guaranteed payments for capital",          "key": None},
    {"line": "6a", "label": "Net short-term capital gain (loss)",       "key": "capital_gains_short"},
    {"line": "9a", "label": "Net long-term capital gain (loss)",        "key": "capital_gains_long"},
    {"line": "18a","label": "Tax-exempt income and nondeductible exp.",  "key": "tax_exempt_income"},
    {"line": "13", "label": "Other deductions",                         "key": "deductions"},
    {"line": "15", "label": "Credits",                                  "key": "credits"},
]


def generate_k1_schema(
    partner_id: str,
    fund_id: str,
    tax_year: int,
    allocations: dict[str, float],
    **kwargs: Any,
) -> dict:
    """Generates an IRS-compatible Schedule K-1 JSON schema for a limited partner.

    Maps standard fund allocation categories to their corresponding Part III
    line items on IRS Form 1065 Schedule K-1. Computes net taxable income
    (ordinary + short-term gains, excluding long-term and exempt).

    Args:
        partner_id: Unique partner identifier string.
        fund_id: Fund entity identifier (EIN or internal system ID).
        tax_year: Four-digit tax year (e.g. 2025).
        allocations: Dict with keys: ordinary_income, capital_gains_short,
            capital_gains_long, tax_exempt_income, deductions, credits.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains k1_json (dict with partner_info, fund_info, allocations,
              line_items), status, and timestamp.
    """
    try:
        required_keys = [
            "ordinary_income", "capital_gains_short", "capital_gains_long",
            "tax_exempt_income", "deductions", "credits",
        ]
        for k in required_keys:
            if k not in allocations:
                raise ValueError(f"Missing required allocation key: {k}")

        line_items: list[dict] = []
        for mapping in _K1_LINE_MAP:
            amount = 0.0
            if mapping["key"] and mapping["key"] in allocations:
                amount = float(allocations[mapping["key"]])
            line_items.append({
                "line": mapping["line"],
                "label": mapping["label"],
                "amount": round(amount, 2),
                "key": mapping["key"],
            })

        net_taxable_income = (
            float(allocations["ordinary_income"])
            + float(allocations["capital_gains_short"])
            - float(allocations["deductions"])
        )

        k1_json: dict[str, Any] = {
            "form": "Schedule K-1 (Form 1065)",
            "tax_year": tax_year,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "partner_info": {
                "partner_id": partner_id,
                "partner_type": "limited_partner",
            },
            "fund_info": {
                "fund_id": fund_id,
                "entity_type": "partnership",
            },
            "allocations": {
                "ordinary_income": round(float(allocations["ordinary_income"]), 2),
                "capital_gains_short": round(float(allocations["capital_gains_short"]), 2),
                "capital_gains_long": round(float(allocations["capital_gains_long"]), 2),
                "tax_exempt_income": round(float(allocations["tax_exempt_income"]), 2),
                "deductions": round(float(allocations["deductions"]), 2),
                "credits": round(float(allocations["credits"]), 2),
                "net_taxable_income": round(net_taxable_income, 2),
            },
            "line_items": line_items,
        }

        return {
            "status": "success",
            "data": {"k1_json": k1_json},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"generate_k1_schema failed: {e}")
        _log_lesson(f"generate_k1_schema: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
