"""
Executive Summary: French AMF token offering whitepaper compliance auditor — validates completeness against Pacte Law (2019) and AMF doctrine, scores required sections, and determines ICO visa/registration requirements.
Inputs: whitepaper_data (dict: token_name, issuer, description, rights_granted, technical_details, risk_factors, use_of_proceeds, team_disclosed)
Outputs: compliant (bool), missing_sections (list), completeness_score (float), amf_registration_required (bool)
MCP Tool Name: france_amf_whitepaper_audit
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "france_amf_whitepaper_audit",
    "description": (
        "Audits a token offering whitepaper against French AMF requirements under the Pacte Law "
        "(Loi n° 2019-486) and AMF General Regulation (RG AMF) Articles 712-1 to 712-23. "
        "Scores completeness, flags missing mandatory sections, and determines ICO visa eligibility."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "whitepaper_data": {
                "type": "object",
                "properties": {
                    "token_name": {"type": "string"},
                    "issuer": {"type": "string"},
                    "description": {"type": "string", "description": "Token description / purpose"},
                    "rights_granted": {
                        "type": "array",
                        "description": "Rights conferred by the token (voting, dividend, access, governance, etc.)",
                        "items": {"type": "string"},
                    },
                    "technical_details": {
                        "type": "boolean",
                        "description": "True if whitepaper includes blockchain/protocol technical specifications",
                    },
                    "risk_factors": {
                        "type": "boolean",
                        "description": "True if whitepaper includes a dedicated risk factors section",
                    },
                    "use_of_proceeds": {
                        "type": "boolean",
                        "description": "True if whitepaper includes breakdown of how funds will be used",
                    },
                    "team_disclosed": {
                        "type": "boolean",
                        "description": "True if team members are identified by name with CVs/backgrounds",
                    },
                    "legal_structure": {
                        "type": "boolean",
                        "description": "True if whitepaper describes the legal entity and governance structure",
                    },
                    "dispute_resolution": {
                        "type": "boolean",
                        "description": "True if whitepaper addresses applicable law and dispute resolution",
                    },
                    "fundraising_cap_eur": {
                        "type": "number",
                        "description": "Maximum fundraising target in EUR (0 = uncapped)",
                    },
                    "investor_protections": {
                        "type": "boolean",
                        "description": "True if whitepaper describes investor protection mechanisms (escrow, smart contract audit, etc.)",
                    },
                    "aml_kyc_procedures": {
                        "type": "boolean",
                        "description": "True if whitepaper describes AML/KYC procedures",
                    },
                    "token_transferable": {
                        "type": "boolean",
                        "description": "True if the token is freely transferable on secondary markets",
                    },
                    "is_security_token": {
                        "type": "boolean",
                        "description": "True if the token grants financial return expectations (may require AMF securities visa instead)",
                    },
                },
                "required": ["token_name", "issuer", "description"],
            }
        },
        "required": ["whitepaper_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "compliant": {"type": "boolean"},
            "missing_sections": {"type": "array", "items": {"type": "string"}},
            "completeness_score": {"type": "number"},
            "amf_registration_required": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "compliant",
            "missing_sections",
            "completeness_score",
            "amf_registration_required",
            "status",
            "timestamp",
        ],
    },
}

# AMF ICO Visa mandatory sections per RG AMF Articles 712-1 to 712-23
# Each entry: (field_key, section_label, weight, citation)
_MANDATORY_SECTIONS: list[tuple[str, str, float, str]] = [
    ("description",          "Token description and purpose",                      0.10, "RG AMF Art. 712-2(1)"),
    ("rights_granted",       "Rights and obligations attached to the token",        0.12, "RG AMF Art. 712-2(2)"),
    ("technical_details",    "Technical characteristics of the blockchain/protocol", 0.08, "RG AMF Art. 712-2(3)"),
    ("risk_factors",         "Risk factors specific to the issuer and offering",    0.15, "RG AMF Art. 712-2(4)"),
    ("use_of_proceeds",      "Breakdown and intended use of funds raised",          0.12, "RG AMF Art. 712-2(5)"),
    ("team_disclosed",       "Identity and experience of management team",          0.10, "RG AMF Art. 712-2(6)"),
    ("legal_structure",      "Legal structure and governance of the issuing entity", 0.10, "RG AMF Art. 712-2(7)"),
    ("dispute_resolution",   "Applicable law and dispute resolution mechanism",     0.06, "RG AMF Art. 712-2(8)"),
    ("investor_protections", "Investor protection mechanisms (escrow, audit, etc.)", 0.10, "RG AMF Art. 712-3 + Doctrine AMF"),
    ("aml_kyc_procedures",   "AML/KYC procedures for token subscribers",            0.07, "LCBFT Art. L561-2 + RG AMF Art. 712-4"),
]


def france_amf_whitepaper_audit(whitepaper_data: dict[str, Any]) -> dict[str, Any]:
    """Audit a token offering whitepaper against French AMF Pacte Law requirements.

    Checks each mandatory section against AMF RG Articles 712-1 to 712-23.
    Calculates a weighted completeness score. Determines AMF visa eligibility
    and whether the offering may constitute a security requiring a different
    regulatory pathway (Prospectus Regulation).

    Args:
        whitepaper_data: Dictionary with token name, issuer, description,
            rights, technical/risk/proceeds/team/legal disclosure booleans,
            fundraising cap, and security token flag.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            compliant (bool): Whether whitepaper meets AMF minimum standard.
            missing_sections (list[str]): Required sections absent or incomplete.
            completeness_score (float): Weighted score from 0.0 to 1.0.
            amf_registration_required (bool): Whether AMF ICO visa is required.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        token_name: str = str(whitepaper_data.get("token_name", ""))
        issuer: str = str(whitepaper_data.get("issuer", ""))
        description: str = str(whitepaper_data.get("description", ""))
        rights_granted: list[str] = whitepaper_data.get("rights_granted", [])
        technical_details: bool = bool(whitepaper_data.get("technical_details", False))
        risk_factors: bool = bool(whitepaper_data.get("risk_factors", False))
        use_of_proceeds: bool = bool(whitepaper_data.get("use_of_proceeds", False))
        team_disclosed: bool = bool(whitepaper_data.get("team_disclosed", False))
        legal_structure: bool = bool(whitepaper_data.get("legal_structure", False))
        dispute_resolution: bool = bool(whitepaper_data.get("dispute_resolution", False))
        fundraising_cap_eur: float = float(whitepaper_data.get("fundraising_cap_eur", 0))
        investor_protections: bool = bool(whitepaper_data.get("investor_protections", False))
        aml_kyc_procedures: bool = bool(whitepaper_data.get("aml_kyc_procedures", False))
        token_transferable: bool = bool(whitepaper_data.get("token_transferable", False))
        is_security_token: bool = bool(whitepaper_data.get("is_security_token", False))

        missing_sections: list[str] = []
        present_weight = 0.0
        total_weight = sum(w for _, _, w, _ in _MANDATORY_SECTIONS)

        # Build a lookup dict for field values
        field_values: dict[str, Any] = {
            "description": len(description) > 50,  # Must be substantive
            "rights_granted": len(rights_granted) > 0,
            "technical_details": technical_details,
            "risk_factors": risk_factors,
            "use_of_proceeds": use_of_proceeds,
            "team_disclosed": team_disclosed,
            "legal_structure": legal_structure,
            "dispute_resolution": dispute_resolution,
            "investor_protections": investor_protections,
            "aml_kyc_procedures": aml_kyc_procedures,
        }

        # Score each section
        section_scores: dict[str, dict[str, Any]] = {}
        for field_key, section_label, weight, citation in _MANDATORY_SECTIONS:
            present = bool(field_values.get(field_key, False))
            section_scores[field_key] = {
                "label": section_label,
                "present": present,
                "weight": weight,
                "citation": citation,
            }
            if present:
                present_weight += weight
            else:
                missing_sections.append(
                    f"MISSING: {section_label} — required by {citation}"
                )

        completeness_score = round(present_weight / total_weight, 3) if total_weight > 0 else 0.0

        # AMF ICO Visa requires at minimum all mandatory sections present and:
        # - Token must NOT be a security (security tokens need Prospectus Regulation)
        # - Fundraising cap disclosure
        # - AMF ICO visa is VOLUNTARY under Pacte Law (but investors look for it)

        # Compliance threshold: all mandatory sections present = score >= 0.85
        _COMPLIANCE_THRESHOLD = 0.85
        compliant = completeness_score >= _COMPLIANCE_THRESHOLD and len(missing_sections) == 0

        # --- AMF Registration Required? ---
        # AMF ICO visa is VOLUNTARY for utility tokens under Pacte Law
        # BUT required if offering to French public and token may be a security
        # OR if issuer wants to use the AMF visa label in marketing
        if is_security_token:
            amf_registration_required = True
            missing_sections.append(
                "CRITICAL: Token appears to be a security (financial return expectation). "
                "AMF Prospectus Regulation (EU) 2017/1129 applies — ICO visa framework "
                "does NOT apply. A prospectus approved by AMF is required for public offer "
                "exceeding EUR 8 million. Engage securities counsel immediately."
            )
        elif fundraising_cap_eur > 8_000_000:
            # Over EUR 8M public offers may trigger Prospectus Regulation regardless
            amf_registration_required = True
            missing_sections.append(
                f"Fundraising cap EUR {fundraising_cap_eur:,.0f} exceeds EUR 8M — "
                "EU Prospectus Regulation (2017/1129) Article 3 threshold may apply "
                "for securities. If utility token, AMF ICO visa strongly recommended "
                "and AMF registration likely required to access French retail investors."
            )
        else:
            # Voluntary AMF ICO visa for utility tokens under Pacte Law Art. 26 / AMF RG Art. 712-1
            amf_registration_required = False
            if not is_security_token:
                missing_sections.append(
                    "ADVISORY: AMF ICO Visa is VOLUNTARY under Pacte Law (Loi PACTE Art. 26). "
                    "Without the visa, the token cannot be marketed to French retail investors. "
                    "AMF visa requires full whitepaper compliance + AMF review (6-8 weeks). "
                    "Strongly recommended if targeting French investors."
                )

        # --- Token Transferability Note ---
        if token_transferable:
            missing_sections.append(
                "NOTE: Token is transferable on secondary markets — assess whether it qualifies "
                "as a financial instrument under MiFID II (jeton/crypto-actif vs titre financier). "
                "French AMF has a formal classification procedure: consult AMF Innovation Hub."
            )

        result = {
            "compliant": compliant,
            "completeness_score": completeness_score,
            "completeness_percentage": round(completeness_score * 100, 1),
            "compliance_threshold": _COMPLIANCE_THRESHOLD,
            "token_name": token_name,
            "issuer": issuer,
            "is_security_token": is_security_token,
            "amf_registration_required": amf_registration_required,
            "section_scores": section_scores,
            "missing_sections": missing_sections,
            "sections_present": sum(1 for s in section_scores.values() if s["present"]),
            "sections_total": len(_MANDATORY_SECTIONS),
            "fundraising_cap_eur": fundraising_cap_eur,
            "key_legislation": [
                "Loi PACTE n° 2019-486 du 22 mai 2019 — Article 26 (ICO framework)",
                "RG AMF Articles 712-1 à 712-23 (ICO whitepaper requirements)",
                "AMF Instruction DOC-2019-06 (ICO visa procedure)",
                "EU Prospectus Regulation (EU) 2017/1129 (if security token)",
                "LCBFT — AML/KYC obligations for ICO issuers",
                "EU MiCA Regulation (EU) 2023/1114 — supersedes national frameworks from 2024",
            ],
            "mica_note": (
                "IMPORTANT: EU MiCA Regulation applies from June 2024 for ARTs and December 2024 "
                "for all other crypto-assets. French AMF ICO visa framework may be superseded by "
                "MiCA crypto-asset whitepaper requirements. Assess which regime applies."
            ),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"france_amf_whitepaper_audit failed: {e}")
        _log_lesson(f"france_amf_whitepaper_audit: {e}")
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
