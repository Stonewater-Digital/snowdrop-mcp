"""
Executive Summary: Generates an ILPA-compliant quarterly LP report in markdown format from fund performance data, with compliance flag detection for missing required fields.

Inputs: fund_data (dict: fund_name, vintage_year, fund_size, nav, tvpi, dpi, irr, top_holdings list, cash_position, next_close_date)
Outputs: dict with ilpa_summary_markdown (str), compliance_flags (list[str])
MCP Tool Name: lp_reporting_standard
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "lp_reporting_standard",
    "description": (
        "Generates an ILPA (Institutional Limited Partners Association) compliant "
        "quarterly fund report in markdown format. Validates presence of all required "
        "ILPA Reporting Template v2 fields and flags any that are missing or null. "
        "Produces structured markdown with sections for Fund Overview, Performance Metrics, "
        "Top Holdings, Cash Position, and Upcoming Events."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_data": {
                "type": "object",
                "properties": {
                    "fund_name": {"type": "string"},
                    "vintage_year": {"type": "integer"},
                    "fund_size": {"type": "number", "description": "Total commitments ($)"},
                    "nav": {"type": "number", "description": "Current net asset value ($)"},
                    "tvpi": {"type": "number", "description": "Total Value to Paid-In multiple"},
                    "dpi": {"type": "number", "description": "Distributions to Paid-In multiple"},
                    "irr": {"type": "number", "description": "Net IRR as decimal (e.g. 0.185)"},
                    "top_holdings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "company": {"type": "string"},
                                "sector": {"type": "string"},
                                "nav": {"type": "number"},
                                "ownership_pct": {"type": "number"}
                            }
                        },
                        "description": "Top portfolio company positions"
                    },
                    "cash_position": {"type": "number", "description": "Cash and equivalents ($)"},
                    "next_close_date": {"type": "string", "description": "Next LP close or reporting date (YYYY-MM-DD)"}
                },
                "required": [
                    "fund_name", "vintage_year", "fund_size", "nav",
                    "tvpi", "dpi", "irr", "top_holdings", "cash_position", "next_close_date"
                ]
            }
        },
        "required": ["fund_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "ilpa_summary_markdown": {"type": "string"},
            "compliance_flags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of missing or invalid required ILPA fields"
            },
            "is_fully_compliant": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["ilpa_summary_markdown", "compliance_flags", "is_fully_compliant", "status", "timestamp"]
    }
}

# ILPA Reporting Template v2 required fields (subset for quarterly LP update)
_ILPA_REQUIRED_FIELDS = [
    "fund_name",
    "vintage_year",
    "fund_size",
    "nav",
    "tvpi",
    "dpi",
    "irr",
    "top_holdings",
    "cash_position",
    "next_close_date",
]


def _fmt_dollars(amount: float | None) -> str:
    """Format a dollar amount with comma separators and M/B suffix.

    Args:
        amount: Dollar amount, or None.

    Returns:
        Formatted string like '$125.5M' or '$1.2B', or 'N/A' if None.
    """
    if amount is None:
        return "N/A"
    if abs(amount) >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    elif abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif abs(amount) >= 1_000:
        return f"${amount:,.0f}"
    else:
        return f"${amount:.2f}"


def _fmt_multiple(val: float | None) -> str:
    """Format a performance multiple.

    Args:
        val: Multiple value, or None.

    Returns:
        Formatted string like '2.1x' or 'N/A'.
    """
    if val is None:
        return "N/A"
    return f"{val:.2f}x"


def _fmt_pct(val: float | None, already_pct: bool = False) -> str:
    """Format a percentage value.

    Args:
        val: Decimal rate (e.g. 0.185) or percentage (e.g. 18.5) depending on already_pct.
        already_pct: If True, val is already a percentage. If False, multiply by 100.

    Returns:
        Formatted string like '18.5%' or 'N/A'.
    """
    if val is None:
        return "N/A"
    pct = val if already_pct else val * 100
    return f"{pct:.1f}%"


def _validate_ilpa_fields(fund_data: dict) -> list[str]:
    """Check for missing or null required ILPA fields.

    Args:
        fund_data: The fund data dictionary to validate.

    Returns:
        List of compliance flag strings, one per missing/invalid field.
        Empty list means fully compliant.
    """
    flags: list[str] = []

    for field in _ILPA_REQUIRED_FIELDS:
        val = fund_data.get(field)
        if val is None:
            flags.append(f"MISSING_FIELD: '{field}' is required by ILPA Reporting Template v2 but not provided")
        elif isinstance(val, str) and not val.strip():
            flags.append(f"EMPTY_FIELD: '{field}' is present but empty")
        elif field == "top_holdings" and (not isinstance(val, list) or len(val) == 0):
            flags.append("MISSING_DATA: 'top_holdings' must be a non-empty list per ILPA standards")

    # Numeric sanity checks
    tvpi = fund_data.get("tvpi")
    dpi = fund_data.get("dpi")
    if tvpi is not None and dpi is not None:
        if dpi > tvpi:
            flags.append(
                f"DATA_ANOMALY: dpi ({dpi:.2f}x) exceeds tvpi ({tvpi:.2f}x) — "
                "DPI cannot exceed TVPI without negative unrealized value"
            )

    irr = fund_data.get("irr")
    if irr is not None and irr < -1.0:
        flags.append(f"DATA_ANOMALY: irr ({irr:.4f}) is below -100% — check decimal vs percentage input")

    nav = fund_data.get("nav")
    fund_size = fund_data.get("fund_size")
    if nav is not None and fund_size is not None and nav > fund_size * 5:
        flags.append(
            f"DATA_ANOMALY: NAV ({_fmt_dollars(nav)}) is >5x fund size ({_fmt_dollars(fund_size)}) — verify inputs"
        )

    return flags


def _build_holdings_table(top_holdings: list[dict]) -> str:
    """Render top holdings as a markdown table.

    Args:
        top_holdings: List of holding dicts with company, sector, nav, ownership_pct.

    Returns:
        Markdown table string.
    """
    if not top_holdings:
        return "_No holdings data provided._\n"

    lines = [
        "| Company | Sector | NAV | Ownership |",
        "|---------|--------|-----|-----------|",
    ]
    for h in top_holdings:
        company = h.get("company", "N/A")
        sector = h.get("sector", "N/A")
        nav = _fmt_dollars(h.get("nav"))
        ownership = _fmt_pct(h.get("ownership_pct"), already_pct=True) if h.get("ownership_pct") is not None else "N/A"
        lines.append(f"| {company} | {sector} | {nav} | {ownership} |")

    return "\n".join(lines) + "\n"


def _build_ilpa_markdown(fund_data: dict, compliance_flags: list[str], report_date: str) -> str:
    """Construct the ILPA-structured markdown report.

    Args:
        fund_data: Validated (or partially validated) fund data dictionary.
        compliance_flags: List of compliance issues to render in the report.
        report_date: ISO 8601 report generation date.

    Returns:
        Full ILPA-compliant markdown report as a string.
    """
    fund_name = fund_data.get("fund_name", "N/A")
    vintage_year = fund_data.get("vintage_year", "N/A")
    fund_size = fund_data.get("fund_size")
    nav = fund_data.get("nav")
    tvpi = fund_data.get("tvpi")
    dpi = fund_data.get("dpi")
    rvpi = round((tvpi or 0) - (dpi or 0), 4) if tvpi is not None and dpi is not None else None
    irr = fund_data.get("irr")
    top_holdings: list[dict] = fund_data.get("top_holdings") or []
    cash_position = fund_data.get("cash_position")
    next_close_date = fund_data.get("next_close_date", "N/A")

    nav_as_pct_size = (
        f" ({nav / fund_size * 100:.1f}% of fund size)" if nav is not None and fund_size else ""
    )

    compliance_section = ""
    if compliance_flags:
        flag_lines = "\n".join(f"- {flag}" for flag in compliance_flags)
        compliance_section = f"""
## Compliance Flags

> **{len(compliance_flags)} issue(s) detected.** This report may not be fully ILPA-compliant.

{flag_lines}

"""
    else:
        compliance_section = """
## Compliance Status

> All required ILPA Reporting Template v2 fields are present and validated.

"""

    holdings_table = _build_holdings_table(top_holdings)

    report = f"""# {fund_name} — Quarterly LP Report

**Report Date:** {report_date}
**Standard:** ILPA Reporting Template v2 (Quarterly Update)

---
{compliance_section}
## Fund Overview

| Field | Value |
|-------|-------|
| Fund Name | {fund_name} |
| Vintage Year | {vintage_year} |
| Fund Size | {_fmt_dollars(fund_size)} |
| Current NAV | {_fmt_dollars(nav)}{nav_as_pct_size} |
| Cash Position | {_fmt_dollars(cash_position)} |

---

## Performance Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| TVPI | {_fmt_multiple(tvpi)} | Total Value to Paid-In |
| DPI | {_fmt_multiple(dpi)} | Distributions to Paid-In (realized) |
| RVPI | {_fmt_multiple(rvpi)} | Residual Value to Paid-In (unrealized) |
| Net IRR | {_fmt_pct(irr)} | Since inception, net of fees and carry |

---

## Top Portfolio Holdings

{holdings_table}

---

## Cash Position

| Item | Amount |
|------|--------|
| Cash & Equivalents | {_fmt_dollars(cash_position)} |
| Cash as % of NAV | {_fmt_pct(cash_position / nav * 100, already_pct=True) if cash_position is not None and nav else 'N/A'} |

---

## Upcoming Events

| Event | Date |
|-------|------|
| Next LP Close / Reporting Date | {next_close_date} |

---

_This report was generated automatically per ILPA Reporting Template v2 standards.
For questions, contact your GP investor relations team._
"""
    return report


def lp_reporting_standard(**kwargs: Any) -> dict:
    """Generate an ILPA-compliant quarterly LP report in markdown format.

    Validates all required ILPA Reporting Template v2 fields, flags any missing
    or anomalous data, and renders a structured markdown document suitable for
    LP distribution. The report follows ILPA's recommended section ordering:
    Fund Overview, Performance Metrics, Top Holdings, Cash Position, Events.

    Args:
        **kwargs: Keyword arguments containing:
            fund_data (dict): Fund performance snapshot with keys:
                - fund_name (str): Legal fund name
                - vintage_year (int): Year of first close
                - fund_size (float): Total LP commitments
                - nav (float): Current net asset value
                - tvpi (float): Total Value to Paid-In
                - dpi (float): Distributions to Paid-In
                - irr (float): Net IRR as decimal (0.185 = 18.5%)
                - top_holdings (list[dict]): Portfolio positions
                - cash_position (float): Cash & equivalents
                - next_close_date (str): Next reporting/close date (YYYY-MM-DD)

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - ilpa_summary_markdown (str): Full ILPA markdown report
                - compliance_flags (list[str]): Missing or invalid field descriptions
                - is_fully_compliant (bool): True if no compliance flags
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        fund_data: dict = kwargs.get("fund_data", {})

        if not fund_data:
            raise ValueError("fund_data is required and cannot be empty")

        report_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        compliance_flags = _validate_ilpa_fields(fund_data)
        is_fully_compliant = len(compliance_flags) == 0

        markdown = _build_ilpa_markdown(fund_data, compliance_flags, report_date)

        result = {
            "ilpa_summary_markdown": markdown,
            "compliance_flags": compliance_flags,
            "is_fully_compliant": is_fully_compliant,
            "n_compliance_issues": len(compliance_flags),
            "report_date": report_date,
            "fund_name": fund_data.get("fund_name", "N/A"),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"lp_reporting_standard failed: {e}")
        _log_lesson(f"lp_reporting_standard: {e}")
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
