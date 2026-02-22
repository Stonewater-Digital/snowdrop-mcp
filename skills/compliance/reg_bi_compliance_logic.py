"""
Executive Summary: SEC Regulation Best Interest (Reg BI) compliance checker — scores the four Reg BI obligations (Disclosure, Care, Conflict of Interest, Compliance) for a broker-dealer recommendation.
Inputs: recommendation (dict: product_name, product_type, fee_pct, risk_level, investor_profile)
Outputs: compliant (bool), obligation_scores (dict), conflicts_identified (list), documentation_requirements (list)
MCP Tool Name: reg_bi_compliance_logic
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "reg_bi_compliance_logic",
    "description": (
        "Evaluates a broker-dealer recommendation against SEC Regulation Best Interest (17 CFR "
        "§ 240.15l-1) four-obligation framework: Disclosure, Care, Conflict of Interest, and "
        "Compliance. Scores each obligation and identifies documentation requirements."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "recommendation": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"},
                    "product_type": {
                        "type": "string",
                        "description": "E.g. mutual_fund, etf, annuity, structured_product, bond, equity, options",
                    },
                    "fee_pct": {
                        "type": "number",
                        "description": "Annual fee / expense ratio as percentage (e.g. 1.25 for 1.25%)",
                    },
                    "risk_level": {
                        "type": "string",
                        "enum": ["low", "moderate", "high", "speculative"],
                    },
                    "has_form_crs": {"type": "boolean", "description": "Was Form CRS provided?"},
                    "has_full_fee_disclosure": {
                        "type": "boolean",
                        "description": "Were all fees and costs fully disclosed?",
                    },
                    "has_conflict_disclosure": {
                        "type": "boolean",
                        "description": "Were all conflicts of interest disclosed?",
                    },
                    "cheaper_alternative_exists": {
                        "type": "boolean",
                        "description": "Does a substantially similar lower-cost alternative exist?",
                    },
                    "cheaper_alternative_considered": {
                        "type": "boolean",
                        "description": "Was the cheaper alternative evaluated and documented?",
                    },
                    "broker_receives_commission": {"type": "boolean"},
                    "revenue_sharing_arrangement": {"type": "boolean"},
                    "proprietary_product": {"type": "boolean"},
                    "investor_profile": {
                        "type": "object",
                        "properties": {
                            "risk_tolerance": {"type": "string", "enum": ["conservative", "moderate", "aggressive"]},
                            "investment_horizon": {"type": "string", "enum": ["short", "medium", "long"]},
                            "net_worth": {"type": "number"},
                            "annual_income": {"type": "number"},
                            "liquidity_needs": {"type": "string", "enum": ["high", "moderate", "low"]},
                            "tax_situation": {"type": "string"},
                            "investment_experience": {
                                "type": "string",
                                "enum": ["none", "limited", "moderate", "sophisticated"],
                            },
                        },
                        "required": ["risk_tolerance", "investment_horizon"],
                    },
                },
                "required": [
                    "product_name",
                    "product_type",
                    "fee_pct",
                    "risk_level",
                    "investor_profile",
                ],
            }
        },
        "required": ["recommendation"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "compliant": {"type": "boolean"},
            "obligation_scores": {"type": "object"},
            "conflicts_identified": {"type": "array", "items": {"type": "string"}},
            "documentation_requirements": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "compliant",
            "obligation_scores",
            "conflicts_identified",
            "documentation_requirements",
            "status",
            "timestamp",
        ],
    },
}

# Fee benchmarks by product type (basis points annualised)
_FEE_BENCHMARKS: dict[str, float] = {
    "etf": 0.20,
    "mutual_fund": 0.85,
    "annuity": 2.50,
    "structured_product": 2.00,
    "bond": 0.50,
    "equity": 0.10,
    "options": 0.75,
    "default": 1.00,
}

# Risk level compatibility matrix: product_risk → acceptable investor risk tolerances
_RISK_COMPATIBILITY: dict[str, set[str]] = {
    "low": {"conservative", "moderate", "aggressive"},
    "moderate": {"moderate", "aggressive"},
    "high": {"aggressive"},
    "speculative": set(),  # Speculative products require special suitability analysis
}


def reg_bi_compliance_logic(recommendation: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a broker-dealer recommendation against the Reg BI four-obligation framework.

    Scores Disclosure, Care, Conflict of Interest, and Compliance obligations
    on a 0.0-1.0 scale. Identifies conflicts of interest and documents required
    written disclosures per SEC Release 34-86031 (Reg BI adopting release).

    Args:
        recommendation: Dictionary with product details, fee structure,
            conflict indicators, and the retail investor's profile.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            compliant (bool): True if all four obligations score >= 0.7.
            obligation_scores (dict): Scores for Disclosure, Care,
                Conflict of Interest, and Compliance (0.0-1.0 each).
            conflicts_identified (list[str]): Specific conflicts found.
            documentation_requirements (list[str]): Required disclosures.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        product_name: str = str(recommendation.get("product_name", ""))
        product_type: str = str(recommendation.get("product_type", "default")).lower()
        fee_pct: float = float(recommendation.get("fee_pct", 0))
        risk_level: str = str(recommendation.get("risk_level", "moderate")).lower()
        has_form_crs: bool = bool(recommendation.get("has_form_crs", False))
        has_full_fee_disclosure: bool = bool(recommendation.get("has_full_fee_disclosure", False))
        has_conflict_disclosure: bool = bool(recommendation.get("has_conflict_disclosure", False))
        cheaper_alt_exists: bool = bool(recommendation.get("cheaper_alternative_exists", False))
        cheaper_alt_considered: bool = bool(recommendation.get("cheaper_alternative_considered", False))
        broker_commission: bool = bool(recommendation.get("broker_receives_commission", False))
        revenue_sharing: bool = bool(recommendation.get("revenue_sharing_arrangement", False))
        proprietary: bool = bool(recommendation.get("proprietary_product", False))
        investor_profile: dict = recommendation.get("investor_profile", {})

        risk_tolerance: str = str(investor_profile.get("risk_tolerance", "moderate")).lower()
        investment_horizon: str = str(investor_profile.get("investment_horizon", "medium")).lower()
        net_worth: float = float(investor_profile.get("net_worth", 0))
        annual_income: float = float(investor_profile.get("annual_income", 0))
        liquidity_needs: str = str(investor_profile.get("liquidity_needs", "moderate")).lower()
        investment_experience: str = str(investor_profile.get("investment_experience", "limited")).lower()

        conflicts_identified: list[str] = []
        documentation_requirements: list[str] = []

        # =====================================================================
        # OBLIGATION 1: DISCLOSURE (Form CRS + material facts)
        # SEC Rule 15l-1(a)(2)(i)
        # =====================================================================
        disclosure_score = 1.0
        disclosure_issues: list[str] = []

        if not has_form_crs:
            disclosure_score -= 0.4
            disclosure_issues.append(
                "Form CRS not provided at or before recommendation (Rule 15l-1(a)(2)(i)(A))"
            )
            documentation_requirements.append(
                "Provide Form CRS (Relationship Summary) to retail investor before or at the "
                "time of recommendation — SEC Exchange Act Rule 17a-14"
            )

        if not has_full_fee_disclosure:
            disclosure_score -= 0.35
            disclosure_issues.append(
                "All fees and costs not fully disclosed in writing before recommendation"
            )
            documentation_requirements.append(
                "Prepare and deliver written disclosure of all fees, costs, and compensation "
                "arrangements (Rule 15l-1(a)(2)(i)(B))"
            )

        if not has_conflict_disclosure:
            disclosure_score -= 0.25
            disclosure_issues.append(
                "Material conflicts of interest not disclosed before recommendation"
            )
            documentation_requirements.append(
                "Disclose in writing all material conflicts of interest before or at time "
                "of recommendation (Rule 15l-1(a)(2)(i)(C))"
            )

        disclosure_score = max(0.0, disclosure_score)

        # =====================================================================
        # OBLIGATION 2: CARE (best interest suitability)
        # SEC Rule 15l-1(a)(2)(ii)
        # =====================================================================
        care_score = 1.0
        care_issues: list[str] = []

        # Risk-tolerance compatibility
        acceptable_risk_tolerances = _RISK_COMPATIBILITY.get(risk_level, set())
        if risk_level == "speculative":
            care_score -= 0.4
            care_issues.append(
                f"Speculative product recommended — requires heightened suitability analysis "
                f"and documented basis that speculation aligns with investor objectives "
                f"(investor risk tolerance: {risk_tolerance})"
            )
        elif risk_tolerance not in acceptable_risk_tolerances:
            care_score -= 0.35
            care_issues.append(
                f"Product risk level '{risk_level}' is inconsistent with investor risk "
                f"tolerance '{risk_tolerance}' (Rule 15l-1(a)(2)(ii)(A) — reasonable basis)"
            )

        # Fee reasonableness
        benchmark_fee = _FEE_BENCHMARKS.get(product_type, _FEE_BENCHMARKS["default"])
        fee_premium_pct = ((fee_pct - benchmark_fee) / benchmark_fee * 100) if benchmark_fee > 0 else 0
        if fee_pct > benchmark_fee * 2.0:
            care_score -= 0.25
            care_issues.append(
                f"Product fee {fee_pct:.2f}% is {fee_premium_pct:.0f}% above the "
                f"{product_type} benchmark of {benchmark_fee:.2f}% — must document why "
                f"this cost is in the investor's best interest"
            )

        # Cheaper alternative analysis
        if cheaper_alt_exists and not cheaper_alt_considered:
            care_score -= 0.20
            care_issues.append(
                "A cheaper substantially similar alternative exists but was not considered "
                "or documented — violates Care Obligation requirement to consider costs "
                "(Rule 15l-1(a)(2)(ii)(B))"
            )
            documentation_requirements.append(
                "Document evaluation of substantially similar lower-cost alternatives and "
                "written rationale for recommending higher-cost product"
            )

        # Liquidity mismatch
        if liquidity_needs == "high" and product_type in {"annuity", "structured_product"}:
            care_score -= 0.20
            care_issues.append(
                f"Investor has high liquidity needs but '{product_type}' products typically "
                "have surrender charges and lock-up periods — potential liquidity mismatch"
            )

        # Investment experience vs product complexity
        if investment_experience in {"none", "limited"} and product_type in {
            "options", "structured_product", "leveraged_etf"
        }:
            care_score -= 0.15
            care_issues.append(
                f"Complex product type '{product_type}' recommended to investor with "
                f"'{investment_experience}' experience — heightened explanation obligation"
            )
            documentation_requirements.append(
                f"Document investor comprehension of '{product_type}' risks including "
                "all downside scenarios and fee structures"
            )

        care_score = max(0.0, care_score)

        # =====================================================================
        # OBLIGATION 3: CONFLICT OF INTEREST
        # SEC Rule 15l-1(a)(2)(iii)
        # =====================================================================
        coi_score = 1.0

        if broker_commission:
            conflicts_identified.append(
                "Broker receives transaction-based commission on this product "
                "(Rule 15l-1(a)(2)(iii) — must identify, disclose, and mitigate)"
            )
            coi_score -= 0.15
            documentation_requirements.append(
                "Written disclosure of commission compensation structure and amount "
                "received by broker for this recommendation"
            )

        if revenue_sharing:
            conflicts_identified.append(
                "Revenue sharing arrangement exists with the product issuer "
                "(shelf space / marketing support payments)"
            )
            coi_score -= 0.20
            documentation_requirements.append(
                "Disclose revenue sharing or marketing support payments received "
                "from product issuer — Form CRS and point-of-sale disclosure"
            )

        if proprietary:
            conflicts_identified.append(
                "Proprietary product recommended — financial incentive to recommend "
                "in-house products over third-party alternatives exists"
            )
            coi_score -= 0.20
            documentation_requirements.append(
                "Document evaluation of equivalent third-party products and written "
                "rationale for recommending proprietary product"
            )

        # Multiple conflicts simultaneously
        active_conflicts = sum([broker_commission, revenue_sharing, proprietary])
        if active_conflicts >= 2:
            conflicts_identified.append(
                f"ELEVATED CONFLICT RISK: {active_conflicts} simultaneous conflicts identified — "
                "consider whether recommendation can be made without triggering conflicts, "
                "or whether a fee-based advisory relationship is more appropriate"
            )
            coi_score -= 0.10

        coi_score = max(0.0, coi_score)

        # =====================================================================
        # OBLIGATION 4: COMPLIANCE POLICIES AND PROCEDURES
        # SEC Rule 15l-1(a)(2)(iv)
        # =====================================================================
        compliance_score = 1.0
        compliance_issues: list[str] = []

        # Without Form CRS, the firm likely lacks a compliant compliance program
        if not has_form_crs:
            compliance_score -= 0.30
            compliance_issues.append(
                "Absence of Form CRS suggests inadequate written policies and procedures "
                "under Rule 15l-1(a)(2)(iv)"
            )

        # Undisclosed conflicts suggest missing conflict mitigation policies
        if not has_conflict_disclosure and len(conflicts_identified) > 0:
            compliance_score -= 0.30
            compliance_issues.append(
                "Conflicts identified but not disclosed — indicates gap in conflict of "
                "interest policies and procedures required by Rule 15l-1(a)(2)(iv)(B)"
            )
            documentation_requirements.append(
                "Establish or update written policies and procedures for identifying, "
                "disclosing, and mitigating conflicts of interest (Rule 15l-1(a)(2)(iv))"
            )

        if cheaper_alt_exists and not cheaper_alt_considered:
            compliance_score -= 0.20
            compliance_issues.append(
                "No comparable product evaluation framework in use — compliance procedures "
                "must require documentation of alternatives analysis"
            )

        compliance_score = max(0.0, compliance_score)

        # =====================================================================
        # OVERALL COMPLIANCE DETERMINATION
        # =====================================================================
        obligation_scores = {
            "disclosure": round(disclosure_score, 2),
            "care": round(care_score, 2),
            "conflict_of_interest": round(coi_score, 2),
            "compliance": round(compliance_score, 2),
        }

        # All four obligations must score >= 0.7 for overall compliance
        _PASSING_SCORE = 0.70
        compliant = all(score >= _PASSING_SCORE for score in obligation_scores.values())

        overall_score = sum(obligation_scores.values()) / len(obligation_scores)

        failing_obligations = [
            name for name, score in obligation_scores.items() if score < _PASSING_SCORE
        ]

        result = {
            "compliant": compliant,
            "overall_score": round(overall_score, 2),
            "passing_threshold": _PASSING_SCORE,
            "obligation_scores": obligation_scores,
            "failing_obligations": failing_obligations,
            "conflicts_identified": conflicts_identified,
            "documentation_requirements": documentation_requirements,
            "product_name": product_name,
            "product_type": product_type,
            "fee_pct": fee_pct,
            "fee_benchmark_pct": _FEE_BENCHMARKS.get(product_type, _FEE_BENCHMARKS["default"]),
            "risk_level": risk_level,
            "investor_risk_tolerance": risk_tolerance,
            "disclosure_issues": disclosure_issues,
            "care_issues": care_issues,
            "compliance_issues": compliance_issues,
            "regulations_checked": [
                "SEC Regulation Best Interest — 17 CFR § 240.15l-1",
                "SEC Exchange Act Rule 17a-14 — Form CRS",
                "SEC Release 34-86031 — Reg BI Adopting Release (June 2019)",
                "FINRA Rule 2111 — Suitability (baseline standard)",
            ],
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"reg_bi_compliance_logic failed: {e}")
        _log_lesson(f"reg_bi_compliance_logic: {e}")
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
