"""
Executive Summary: Indian GST calculator for international financial and technology services — applies correct GST rates for domestic, SEZ, and export scenarios including OIDAR special rules.
Inputs: service_type (str), service_value_inr (float), recipient_location (str), is_oidar (bool)
Outputs: gst_amount (float), effective_rate (float), exemptions_applied (list), filing_requirements (list)
MCP Tool Name: india_gst_tax_calculator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "india_gst_tax_calculator",
    "description": (
        "Calculates Indian Goods and Services Tax (GST) for services including cross-border "
        "supply, SEZ, and export scenarios. Applies IGST Act 2017 rates, OIDAR (Online "
        "Information Database Access and Retrieval) rules, and LUT (Letter of Undertaking) "
        "exemptions for zero-rated exports."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "service_type": {
                "type": "string",
                "description": "Type of service: financial_services / software / consulting / cloud / data_analytics / fintech / other",
            },
            "service_value_inr": {
                "type": "number",
                "description": "Transaction value in Indian Rupees (INR)",
            },
            "recipient_location": {
                "type": "string",
                "description": "Recipient jurisdiction: 'domestic' / 'sez' (Special Economic Zone) / 'export' (outside India)",
                "enum": ["domestic", "sez", "export"],
            },
            "is_oidar": {
                "type": "boolean",
                "description": "True if the service is Online Information Database Access and Retrieval (OIDAR)",
            },
            "has_lut": {
                "type": "boolean",
                "description": "True if a valid Letter of Undertaking (LUT) is filed with GST authority (required for zero-rated export without paying IGST)",
                "default": True,
            },
            "recipient_is_registered": {
                "type": "boolean",
                "description": "True if the domestic recipient is a GST-registered business (B2B vs B2C changes reverse charge applicability)",
                "default": False,
            },
            "state_of_supplier": {
                "type": "string",
                "description": "State code of the supplier (for CGST/SGST vs IGST determination, e.g. 'MH', 'KA', 'DL')",
                "default": "MH",
            },
        },
        "required": ["service_type", "service_value_inr", "recipient_location", "is_oidar"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "gst_amount": {"type": "number"},
            "effective_rate": {"type": "number"},
            "exemptions_applied": {"type": "array", "items": {"type": "string"}},
            "filing_requirements": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "gst_amount",
            "effective_rate",
            "exemptions_applied",
            "filing_requirements",
            "status",
            "timestamp",
        ],
    },
}

# GST rates (IGST Schedule / Notification No. 11/2017-IGST)
_GST_RATES: dict[str, float] = {
    "financial_services": 18.0,        # Banking, insurance, investment advisory
    "software": 18.0,                  # Software development, IT services
    "consulting": 18.0,                # Management consulting, legal
    "cloud": 18.0,                     # SaaS, PaaS, IaaS
    "data_analytics": 18.0,            # Data processing, analytics
    "fintech": 18.0,                   # Payment gateways, robo-advisory
    "healthcare": 0.0,                 # Healthcare services — exempt (Notification 12/2017)
    "education": 0.0,                  # Educational services — exempt
    "agriculture": 0.0,                # Agricultural services — exempt
    "other": 18.0,                     # Default rate for services
}

# OIDAR services: digital services provided over internet (Sec 2(17) IGST Act)
# B2C OIDAR to recipients in India: supplier must register and pay IGST
# B2B OIDAR to registered recipients: reverse charge applies
_OIDAR_RATE = 18.0


def india_gst_tax_calculator(
    service_type: str,
    service_value_inr: float,
    recipient_location: str,
    is_oidar: bool,
    has_lut: bool = True,
    recipient_is_registered: bool = False,
    state_of_supplier: str = "MH",
) -> dict[str, Any]:
    """Calculate Indian GST liability for a service transaction.

    Applies IGST Act 2017 and CGST Act 2017 rules for domestic, SEZ, and
    export supply of services. Handles the OIDAR regime for digital services
    and LUT-based zero-rating for exports.

    Args:
        service_type: Category of service (e.g. "financial_services", "cloud").
        service_value_inr: Transaction value in Indian Rupees.
        recipient_location: "domestic", "sez", or "export".
        is_oidar: Whether the service qualifies as OIDAR under IGST Act s. 2(17).
        has_lut: Whether a valid Letter of Undertaking is on file (enables
            zero-rated export without paying IGST upfront).
        recipient_is_registered: Whether the domestic recipient holds a GSTIN.
        state_of_supplier: Supplier state code (affects CGST/SGST split vs IGST).

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            gst_amount (float): Total GST payable in INR.
            effective_rate (float): Effective GST rate applied (0-18%).
            exemptions_applied (list[str]): Exemptions or zero-rating applied.
            filing_requirements (list[str]): Mandatory GST return filings.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        service_type = str(service_type).lower().replace(" ", "_")
        service_value_inr = float(service_value_inr)
        recipient_location = str(recipient_location).lower().strip()
        is_oidar = bool(is_oidar)
        has_lut = bool(has_lut)
        recipient_is_registered = bool(recipient_is_registered)

        exemptions_applied: list[str] = []
        filing_requirements: list[str] = []
        gst_breakdown: dict[str, float] = {}

        # --- Determine Base GST Rate ---
        if is_oidar:
            base_rate = _OIDAR_RATE
        else:
            base_rate = _GST_RATES.get(service_type, _GST_RATES["other"])

        effective_rate = base_rate

        # =====================================================================
        # EXPORT OF SERVICES (Zero-Rated Supply — Sec 16 IGST Act 2017)
        # =====================================================================
        if recipient_location == "export":
            if has_lut:
                # Zero-rated supply with LUT: no IGST payable, ITC refund available
                effective_rate = 0.0
                gst_amount = 0.0
                exemptions_applied.append(
                    "Zero-rated supply under IGST Act Section 16(3)(a): Export of services with "
                    "Letter of Undertaking (LUT). No IGST payable. Input tax credit (ITC) "
                    "refund available for taxes paid on inputs."
                )
                exemptions_applied.append(
                    "LUT filed under Rule 96A CGST Rules — valid for one financial year. "
                    "Renewal required by 1st April each year."
                )
                filing_requirements.extend([
                    "GSTR-1: Report export invoice with shipping bill/bill of export number",
                    "GSTR-3B: Monthly return — report zero-rated exports",
                    "GSTR-9: Annual return (if aggregate turnover > INR 2 crore)",
                    "RFD-01: ITC refund application within 2 years of export",
                    "Maintain Foreign Inward Remittance Certificate (FIRC) as proof of export proceeds",
                ])
            else:
                # Export without LUT: pay IGST upfront, then claim refund (Sec 16(3)(b))
                effective_rate = base_rate
                gst_amount = service_value_inr * (effective_rate / 100)
                exemptions_applied.append(
                    "Export of services without LUT: IGST paid upfront under IGST Act Section 16(3)(b). "
                    "Refund claimable after export is validated. Consider filing LUT to avoid cash flow impact."
                )
                filing_requirements.extend([
                    "GSTR-1: Report export invoice with IGST amount",
                    "GSTR-3B: Pay IGST on export",
                    "RFD-01: Claim IGST refund after export realisation (within 2 years)",
                    "Recommend filing LUT (Form RFD-11) before next export to eliminate IGST outflow",
                ])
                gst_breakdown = {
                    "igst": gst_amount,
                    "cgst": 0.0,
                    "sgst": 0.0,
                }

        # =====================================================================
        # SEZ SUPPLY (Zero-Rated Supply — Sec 16(1)(b) IGST Act 2017)
        # =====================================================================
        elif recipient_location == "sez":
            # Supply to SEZ unit/developer treated as zero-rated
            effective_rate = 0.0
            gst_amount = 0.0
            exemptions_applied.append(
                "Zero-rated supply to Special Economic Zone (SEZ) unit/developer under "
                "IGST Act Section 16(1)(b). No GST payable. ITC refund available."
            )
            exemptions_applied.append(
                "Supply must be accompanied by endorsement from SEZ Specified Officer "
                "(Form A-1) confirming the recipient is an SEZ unit/developer."
            )
            filing_requirements.extend([
                "GSTR-1: Report SEZ supply with relevant endorsement details",
                "GSTR-3B: Report zero-rated SEZ supply",
                "Maintain SEZ endorsement documentation for 6 years",
                "LUT filing recommended to avoid paying IGST with refund claim",
            ])

        # =====================================================================
        # DOMESTIC SUPPLY — IGST or CGST+SGST
        # =====================================================================
        elif recipient_location == "domestic":

            # OIDAR B2C domestic: overseas supplier must register and pay IGST
            if is_oidar and not recipient_is_registered:
                effective_rate = _OIDAR_RATE
                gst_amount = service_value_inr * (effective_rate / 100)
                exemptions_applied.append(
                    "OIDAR B2C supply: overseas digital service provider must register "
                    "under IGST Act Section 14. IGST collected directly from end-consumer."
                )
                gst_breakdown = {"igst": gst_amount, "cgst": 0.0, "sgst": 0.0}
                filing_requirements.extend([
                    "OIDAR Simplified Registration via GST Portal (for overseas OIDAR providers)",
                    "GSTR-5A: Quarterly return for OIDAR providers (due 20th of month following quarter)",
                    "IGST deposit by 20th of following month",
                ])

            elif is_oidar and recipient_is_registered:
                # B2B OIDAR: reverse charge applies — recipient pays IGST
                effective_rate = _OIDAR_RATE
                gst_amount = service_value_inr * (effective_rate / 100)
                exemptions_applied.append(
                    "OIDAR B2B supply: Reverse Charge Mechanism (RCM) applies under "
                    "IGST Act Section 5(3). GST-registered recipient must self-assess "
                    "and pay IGST directly. Overseas supplier exempt from Indian GST registration."
                )
                gst_breakdown = {"igst": gst_amount, "cgst": 0.0, "sgst": 0.0}
                filing_requirements.extend([
                    "RECIPIENT: GSTR-3B — pay IGST under reverse charge by 20th of next month",
                    "RECIPIENT: GSTR-2B — reconcile inward RCM supplies",
                    "SUPPLIER: No Indian GST registration required if all supplies are B2B",
                ])

            else:
                # Standard domestic service supply
                effective_rate = base_rate
                gst_amount = service_value_inr * (effective_rate / 100)

                # Determine IGST vs CGST+SGST based on supply type
                # Inter-state (supplier and recipient in different states) → IGST
                # Intra-state → CGST + SGST (split 50/50)
                # For services, place of supply = location of recipient
                cgst_rate = effective_rate / 2
                sgst_rate = effective_rate / 2
                igst_rate = effective_rate

                gst_breakdown = {
                    "igst": 0.0,
                    "cgst": service_value_inr * (cgst_rate / 100),
                    "sgst_utst": service_value_inr * (sgst_rate / 100),
                }

                filing_requirements.extend([
                    "GSTR-1: Report B2B/B2C supply by 11th of following month (monthly) or 13th (quarterly QRMP)",
                    "GSTR-3B: Monthly summary and tax payment by 20th of following month",
                    "E-Invoice: Mandatory if aggregate turnover > INR 10 crore (Notification 70/2023)",
                ])

                if base_rate == 0.0:
                    exemptions_applied.append(
                        f"Service type '{service_type}' is exempt from GST under CGST/IGST "
                        "Exemption Notification (Notification 12/2017-CT(Rate))"
                    )
                    gst_amount = 0.0
                    effective_rate = 0.0
                    gst_breakdown = {"igst": 0.0, "cgst": 0.0, "sgst": 0.0}

        else:
            return {
                "status": "error",
                "error": f"Invalid recipient_location '{recipient_location}'. Must be 'domestic', 'sez', or 'export'.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Final gst_amount resolution
        if recipient_location in {"export", "sez"} and has_lut:
            gst_amount = 0.0

        result = {
            "gst_amount": round(gst_amount, 2),
            "effective_rate": effective_rate,
            "service_type": service_type,
            "service_value_inr": service_value_inr,
            "recipient_location": recipient_location,
            "is_oidar": is_oidar,
            "has_lut": has_lut,
            "recipient_is_registered": recipient_is_registered,
            "gst_breakdown": gst_breakdown,
            "exemptions_applied": exemptions_applied,
            "filing_requirements": filing_requirements,
            "legislation": [
                "IGST Act 2017 — Section 2(17) OIDAR, Section 16 Zero-Rating",
                "CGST Act 2017 — Section 5(3) Reverse Charge",
                "CGST Rules 2017 — Rule 96A Letter of Undertaking",
                "Notification 11/2017-CT(Rate) — GST rate schedule for services",
                "Notification 12/2017-CT(Rate) — Exempt services",
                "IGST Act Section 14 — Online information and database access services",
            ],
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"india_gst_tax_calculator failed: {e}")
        _log_lesson(f"india_gst_tax_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


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
