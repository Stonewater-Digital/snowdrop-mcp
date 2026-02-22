"""
Executive Summary: Irish ICAV (Irish Collective Asset-management Vehicle) CBI reporting generator — produces structured CBI fund reporting data, checks UCITS/AIFMD compliance flags, and lists upcoming filing deadlines.
Inputs: fund_data (dict: icav_name, sub_funds, nav, domicile, management_company, depositary, reporting_period)
Outputs: cbi_report_json (dict), regulatory_status (str), filings_due (list of dicts)
MCP Tool Name: ireland_ica_reporting
"""
import os
import logging
from typing import Any
from datetime import datetime, date, timezone
from dateutil.relativedelta import relativedelta  # type: ignore

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ireland_ica_reporting",
    "description": (
        "Generates Irish Central Bank (CBI) reporting data for Irish Collective Asset-management "
        "Vehicles (ICAVs) under the Irish Collective Asset-management Vehicles Act 2015 and "
        "CBI UCITS/AIF Rulebooks. Supports both UCITS and AIFMD structures with sub-fund "
        "disaggregation and CBI deadline computation."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_data": {
                "type": "object",
                "properties": {
                    "icav_name": {"type": "string"},
                    "sub_funds": {
                        "type": "array",
                        "description": "List of sub-fund details",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "strategy": {"type": "string"},
                                "nav": {"type": "number"},
                                "currency": {"type": "string"},
                                "investor_type": {"type": "string", "enum": ["retail", "professional", "both"]},
                            },
                        },
                    },
                    "nav": {"type": "number", "description": "Total umbrella NAV in EUR"},
                    "domicile": {"type": "string", "description": "Must be 'IE' for ICAV"},
                    "management_company": {"type": "string", "description": "Name of the AIFM or UCITS ManCo"},
                    "depositary": {"type": "string", "description": "Name of the appointed depositary"},
                    "reporting_period": {
                        "type": "string",
                        "description": "End date of the reporting period YYYY-MM-DD",
                    },
                    "fund_type": {
                        "type": "string",
                        "description": "ucits / aif / qiaif (Qualifying Investor AIF)",
                        "enum": ["ucits", "aif", "qiaif"],
                    },
                    "authorized_date": {
                        "type": "string",
                        "description": "CBI authorisation date YYYY-MM-DD",
                    },
                    "aum_eur": {
                        "type": "number",
                        "description": "AUM for AIFMD Large Manager threshold check (EUR)",
                    },
                    "uses_leverage": {"type": "boolean"},
                    "leverage_method": {
                        "type": "string",
                        "enum": ["commitment", "gross", "both", "none"],
                        "default": "none",
                    },
                    "has_prime_broker": {"type": "boolean"},
                    "ucits_compliant_investments": {
                        "type": "boolean",
                        "description": "True if all investments comply with UCITS eligible asset rules",
                    },
                },
                "required": [
                    "icav_name",
                    "nav",
                    "management_company",
                    "depositary",
                    "reporting_period",
                    "fund_type",
                ],
            }
        },
        "required": ["fund_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "cbi_report_json": {"type": "object"},
            "regulatory_status": {"type": "string"},
            "filings_due": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "filing_name": {"type": "string"},
                        "deadline": {"type": "string"},
                    },
                },
            },
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["cbi_report_json", "regulatory_status", "filings_due", "status", "timestamp"],
    },
}

# AIFMD large manager threshold (AIFMD Article 3(2)) — EUR 100M (leveraged) or EUR 500M (unleveraged)
_AIFMD_LARGE_MANAGER_LEVERAGED_EUR = 100_000_000
_AIFMD_LARGE_MANAGER_UNLEVERAGED_EUR = 500_000_000


def ireland_ica_reporting(fund_data: dict[str, Any]) -> dict[str, Any]:
    """Generate CBI reporting data for an Irish ICAV fund structure.

    Compiles regulatory metadata, checks UCITS/AIFMD compliance flags,
    assesses large manager status, and computes all upcoming CBI filing
    deadlines relative to the reporting period end date.

    Args:
        fund_data: Dictionary with ICAV name, sub-funds, NAV, management
            company, depositary, reporting period, fund type, and
            operational parameters including leverage and prime broker.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            cbi_report_json (dict): Structured CBI reporting payload.
            regulatory_status (str): UCITS/AIFMD compliance assessment.
            filings_due (list[dict]): Upcoming CBI filings with deadlines.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        icav_name: str = str(fund_data.get("icav_name", ""))
        sub_funds: list[dict] = fund_data.get("sub_funds", [])
        nav: float = float(fund_data.get("nav", 0))
        domicile: str = str(fund_data.get("domicile", "IE")).upper()
        management_company: str = str(fund_data.get("management_company", ""))
        depositary: str = str(fund_data.get("depositary", ""))
        reporting_period: str = str(fund_data.get("reporting_period", ""))
        fund_type: str = str(fund_data.get("fund_type", "aif")).lower()
        authorized_date: str = str(fund_data.get("authorized_date", ""))
        aum_eur: float = float(fund_data.get("aum_eur", nav))
        uses_leverage: bool = bool(fund_data.get("uses_leverage", False))
        leverage_method: str = str(fund_data.get("leverage_method", "none")).lower()
        has_prime_broker: bool = bool(fund_data.get("has_prime_broker", False))
        ucits_compliant: bool = bool(fund_data.get("ucits_compliant_investments", True))

        compliance_flags: list[str] = []
        regulatory_status = "COMPLIANT"

        # --- Domicile Check ---
        if domicile != "IE":
            compliance_flags.append(
                f"WARNING: ICAV domicile must be Ireland ('IE'). Reported domicile: '{domicile}'. "
                "An ICAV is constituted under Irish law only (ICAV Act 2015, s.6)."
            )
            regulatory_status = "NON_COMPLIANT"

        # --- Fund Type-Specific Checks ---
        if fund_type == "ucits":
            # UCITS must comply with CBI UCITS Regulations 2011 (SI 352/2011)
            if not ucits_compliant:
                compliance_flags.append(
                    "UCITS: Investment universe contains non-eligible assets "
                    "(CBI UCITS Regulations 2011 Reg. 68 — eligible assets must be "
                    "transferable securities, money market instruments, collective investment "
                    "schemes, deposits, derivatives on regulated markets)."
                )
                regulatory_status = "NON_COMPLIANT"
            if uses_leverage:
                compliance_flags.append(
                    "UCITS leverage: Global exposure must be calculated daily via "
                    "commitment or VaR approach (CBI UCITS Reg. 134-135). "
                    "VaR limit: absolute VaR ≤ 20% NAV or relative VaR ≤ 2× benchmark."
                )
            if has_prime_broker:
                compliance_flags.append(
                    "NOTE: UCITS may not appoint a prime broker in the traditional sense. "
                    "Prime brokerage services permissible only within ESMA UCITS guidelines "
                    "on ETFs and other UCITS issues (ESMA/2014/937)."
                )

        elif fund_type in {"aif", "qiaif"}:
            # AIFMD large manager check
            large_manager = (
                (uses_leverage and aum_eur > _AIFMD_LARGE_MANAGER_LEVERAGED_EUR)
                or (not uses_leverage and aum_eur > _AIFMD_LARGE_MANAGER_UNLEVERAGED_EUR)
            )
            if large_manager:
                compliance_flags.append(
                    f"AIFMD Large AIFM: AUM EUR {aum_eur:,.0f} exceeds threshold "
                    f"({'EUR 100M (leveraged)' if uses_leverage else 'EUR 500M (unleveraged)'}) — "
                    "full AIFMD authorisation required (AIFMD Art. 3(2), CBI AIFMD Rulebook). "
                    "Quarterly reporting to CBI + Annex IV to ESMA/national regulators."
                )

            if fund_type == "qiaif":
                compliance_flags.append(
                    "QIAIF: Qualifying Investor AIF — minimum EUR 100,000 subscription per investor. "
                    "Must be offered only to Qualifying Investors (CBI AIF Rulebook Appendix I). "
                    "No prospectus requirement but offering document must be approved by CBI."
                )

        # --- Depositary Check ---
        if not depositary:
            compliance_flags.append(
                "CRITICAL: No depositary appointed. Depositary is mandatory for all UCITS and AIFs "
                "(UCITS V Directive Art. 22; AIFMD Art. 21). Must be a credit institution or "
                "investment firm authorised in Ireland or EEA with Irish branch."
            )
            regulatory_status = "NON_COMPLIANT"

        # --- Sub-Fund Disaggregation ---
        sub_fund_reports = []
        for sf in sub_funds:
            sf_report = {
                "sub_fund_name": sf.get("name", ""),
                "strategy": sf.get("strategy", ""),
                "nav_eur": sf.get("nav", 0),
                "currency": sf.get("currency", "EUR"),
                "investor_type": sf.get("investor_type", "professional"),
                "cbi_reporting_unit": "Sub-Fund",
            }
            sub_fund_reports.append(sf_report)

        # --- CBI Report JSON ---
        cbi_report_json = {
            "report_type": "CBI Fund Annual / Periodic Report",
            "icav_name": icav_name,
            "domicile": domicile,
            "fund_type": fund_type.upper(),
            "reporting_period_end": reporting_period,
            "management_company": management_company,
            "depositary": depositary,
            "authorized_date": authorized_date,
            "total_nav_eur": nav,
            "total_aum_eur": aum_eur,
            "number_of_sub_funds": len(sub_funds),
            "sub_funds": sub_fund_reports,
            "uses_leverage": uses_leverage,
            "leverage_method": leverage_method,
            "has_prime_broker": has_prime_broker,
            "compliance_flags": compliance_flags,
            "regulatory_status": regulatory_status,
            "reporting_standards": [
                "ICAV Act 2015",
                "CBI UCITS Regulations 2011 (SI 352/2011)" if fund_type == "ucits" else "CBI AIF Rulebook",
                "AIFMD (2011/61/EU)" if fund_type in {"aif", "qiaif"} else "UCITS V Directive (2014/91/EU)",
            ],
        }

        # --- Filing Deadlines ---
        filings_due = _compute_filing_deadlines(reporting_period, fund_type, uses_leverage, aum_eur)

        if not compliance_flags:
            regulatory_status = "COMPLIANT — No material issues detected"

        result = {
            "cbi_report_json": cbi_report_json,
            "regulatory_status": regulatory_status,
            "filings_due": filings_due,
            "compliance_flags": compliance_flags,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"ireland_ica_reporting failed: {e}")
        _log_lesson(f"ireland_ica_reporting: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _compute_filing_deadlines(
    reporting_period: str,
    fund_type: str,
    uses_leverage: bool,
    aum_eur: float,
) -> list[dict[str, str]]:
    """Compute upcoming CBI filing deadlines from the reporting period end date.

    Args:
        reporting_period: ISO-8601 date string (YYYY-MM-DD) for period end.
        fund_type: "ucits", "aif", or "qiaif".
        uses_leverage: Whether the fund uses leverage (affects Annex IV frequency).
        aum_eur: AUM in EUR (affects large manager determination).

    Returns:
        List of dicts with filing_name and deadline keys.
    """
    filings: list[dict[str, str]] = []

    try:
        period_end = date.fromisoformat(reporting_period)
    except (ValueError, TypeError):
        period_end = date.today()

    # Annual report: 4 months after year end for UCITS; 6 months for AIFs
    if fund_type == "ucits":
        annual_deadline = period_end + relativedelta(months=4)
        filings.append({
            "filing_name": "UCITS Annual Report (CBI UCITS Reg. 79)",
            "deadline": annual_deadline.isoformat(),
            "frequency": "annual",
        })
        semi_annual_deadline = period_end + relativedelta(months=2)
        filings.append({
            "filing_name": "UCITS Semi-Annual Report (CBI UCITS Reg. 79)",
            "deadline": semi_annual_deadline.isoformat(),
            "frequency": "semi-annual",
        })
        filings.append({
            "filing_name": "CBI Annual Regulatory Return (online filing)",
            "deadline": (period_end + relativedelta(months=3)).isoformat(),
            "frequency": "annual",
        })
    else:
        # AIF/QIAIF
        annual_deadline = period_end + relativedelta(months=6)
        filings.append({
            "filing_name": "AIF Annual Report (AIFMD Art. 22)",
            "deadline": annual_deadline.isoformat(),
            "frequency": "annual",
        })

        # AIFMD Annex IV reporting frequency
        is_large = (uses_leverage and aum_eur > _AIFMD_LARGE_MANAGER_LEVERAGED_EUR) or \
                   (not uses_leverage and aum_eur > _AIFMD_LARGE_MANAGER_UNLEVERAGED_EUR)
        if is_large:
            # Large AIFMs: quarterly Annex IV (due 1 month after quarter end)
            for q in range(1, 5):
                q_end = period_end + relativedelta(months=3 * q)
                filings.append({
                    "filing_name": f"AIFMD Annex IV Quarterly Report (Large AIFM) — Q{q}",
                    "deadline": (q_end + relativedelta(months=1)).isoformat(),
                    "frequency": "quarterly",
                })
        else:
            # Small/sub-threshold AIFMs: annual Annex IV
            filings.append({
                "filing_name": "AIFMD Annex IV Annual Report (sub-threshold AIFM)",
                "deadline": (period_end + relativedelta(months=2)).isoformat(),
                "frequency": "annual",
            })

    # CBI Online Reporting System (ONR) — annual statistics
    filings.append({
        "filing_name": "CBI Investment Funds Statistics Report (ONR system)",
        "deadline": (period_end + relativedelta(months=1)).isoformat(),
        "frequency": "monthly",
        "notes": "Monthly NAV and investor data to CBI via ONR portal",
    })

    # ECB EMIR trade reporting (if applicable)
    filings.append({
        "filing_name": "EMIR Trade Repository Reporting (if derivatives used)",
        "deadline": "T+1 business day",
        "frequency": "daily",
        "notes": "Mandatory if fund uses OTC or ETD derivatives (EMIR Art. 9)",
    })

    return filings


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception:
        pass
