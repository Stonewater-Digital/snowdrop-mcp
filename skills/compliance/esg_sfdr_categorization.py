"""
Executive Summary: EU SFDR fund Article 6/8/9 categorization engine — classifies investment funds under the Sustainable Finance Disclosure Regulation based on ESG integration, sustainable objectives, taxonomy alignment, and benchmark type.
Inputs: fund_data (dict: fund_name, esg_integration, promotes_esg, sustainable_objective, taxonomy_alignment_pct, principal_adverse_impacts, benchmark_type)
Outputs: article_classification (str), disclosure_requirements (list), taxonomy_reporting_required (bool), pai_statement_required (bool)
MCP Tool Name: esg_sfdr_categorization
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "esg_sfdr_categorization",
    "description": (
        "Classifies EU investment funds under SFDR (EU) 2019/2088 as Article 6 (no ESG), "
        "Article 8 (promotes ESG characteristics), or Article 9 (sustainable investment objective). "
        "Applies ESA Joint Supervisory Authority guidance, ESMA Q&A, and EU Taxonomy Regulation "
        "(EU) 2020/852 disclosure requirements."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_data": {
                "type": "object",
                "properties": {
                    "fund_name": {"type": "string"},
                    "esg_integration": {
                        "type": "boolean",
                        "description": "True if ESG factors are considered in investment process (SFDR Art. 6)",
                    },
                    "promotes_esg": {
                        "type": "boolean",
                        "description": "True if fund promotes environmental or social characteristics (SFDR Art. 8)",
                    },
                    "sustainable_objective": {
                        "type": "boolean",
                        "description": "True if fund has sustainable investment as its objective (SFDR Art. 9)",
                    },
                    "taxonomy_alignment_pct": {
                        "type": "number",
                        "description": "Percentage of investments aligned with EU Taxonomy (0-100)",
                    },
                    "principal_adverse_impacts": {
                        "type": "boolean",
                        "description": "True if fund considers Principal Adverse Impacts (PAI) on sustainability factors",
                    },
                    "benchmark_type": {
                        "type": ["string", "null"],
                        "description": "null / eu_climate_transition / eu_paris_aligned / esg_benchmark / other",
                    },
                    "minimum_sustainable_investment_pct": {
                        "type": "number",
                        "description": "Minimum % of portfolio in sustainable investments (0-100)",
                        "default": 0,
                    },
                    "dnsh_assessment": {
                        "type": "boolean",
                        "description": "True if Do No Significant Harm (DNSH) assessment is performed on investments",
                    },
                    "good_governance_checked": {
                        "type": "boolean",
                        "description": "True if investee companies are screened for good governance practices",
                    },
                    "has_engagement_policy": {
                        "type": "boolean",
                        "description": "True if fund has a shareholder engagement / stewardship policy",
                    },
                    "sfdr_entity_type": {
                        "type": "string",
                        "description": "ucits / aif / pension / insurance_ibip / other",
                        "default": "ucits",
                    },
                },
                "required": [
                    "fund_name",
                    "esg_integration",
                    "promotes_esg",
                    "sustainable_objective",
                    "taxonomy_alignment_pct",
                    "principal_adverse_impacts",
                ],
            }
        },
        "required": ["fund_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "article_classification": {"type": "string"},
            "disclosure_requirements": {"type": "array", "items": {"type": "string"}},
            "taxonomy_reporting_required": {"type": "boolean"},
            "pai_statement_required": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "article_classification",
            "disclosure_requirements",
            "taxonomy_reporting_required",
            "pai_statement_required",
            "status",
            "timestamp",
        ],
    },
}

# SFDR taxonomy alignment disclosure thresholds
_TAXONOMY_REPORTING_THRESHOLD = 0.0  # Any Art. 8/9 fund must disclose taxonomy alignment
_ART9_MIN_SUSTAINABLE_INVESTMENT = 80.0  # Art. 9 funds should have high sustainable investment %

# ESAs Q&A: Art. 8+ means Art. 8 fund with significant sustainable investment commitment
_ART8_PLUS_MIN_SUSTAINABLE_PCT = 1.0  # Has at least some sustainable investment commitment

# PAI statement mandatory for: financial market participants with >500 employees OR voluntary opt-in
_PAI_MANDATORY_EMPLOYEE_THRESHOLD = 500


def esg_sfdr_categorization(fund_data: dict[str, Any]) -> dict[str, Any]:
    """Classify an investment fund under SFDR Articles 6, 8, or 9.

    Applies the SFDR classification waterfall: Article 9 (sustainable objective)
    takes precedence over Article 8 (promotes ESG), which takes precedence over
    Article 6 (no ESG claims). Validates Art. 9 quality requirements including
    DNSH, good governance, and minimum sustainable investment percentage.

    Args:
        fund_data: Dictionary with fund ESG attributes including integration,
            promotion, sustainable objective, taxonomy alignment, PAI
            consideration, benchmark type, and DNSH status.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            article_classification (str): "6", "8", "8+", or "9".
            disclosure_requirements (list[str]): SFDR and Taxonomy disclosures
                required for this classification.
            taxonomy_reporting_required (bool): Whether EU Taxonomy alignment
                disclosure is required.
            pai_statement_required (bool): Whether a PAI statement is required.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        fund_name: str = str(fund_data.get("fund_name", ""))
        esg_integration: bool = bool(fund_data.get("esg_integration", False))
        promotes_esg: bool = bool(fund_data.get("promotes_esg", False))
        sustainable_objective: bool = bool(fund_data.get("sustainable_objective", False))
        taxonomy_alignment_pct: float = float(fund_data.get("taxonomy_alignment_pct", 0))
        pai_considered: bool = bool(fund_data.get("principal_adverse_impacts", False))
        benchmark_type: str | None = fund_data.get("benchmark_type")
        min_sustainable_pct: float = float(fund_data.get("minimum_sustainable_investment_pct", 0))
        dnsh_assessment: bool = bool(fund_data.get("dnsh_assessment", False))
        good_governance_checked: bool = bool(fund_data.get("good_governance_checked", False))
        has_engagement_policy: bool = bool(fund_data.get("has_engagement_policy", False))
        sfdr_entity_type: str = str(fund_data.get("sfdr_entity_type", "ucits")).lower()

        disclosure_requirements: list[str] = []
        quality_warnings: list[str] = []

        # =====================================================================
        # SFDR CLASSIFICATION WATERFALL
        # =====================================================================

        # --- ARTICLE 9: Sustainable Investment Objective ---
        # SFDR Art. 9(1): fund has sustainable investment as its primary objective
        if sustainable_objective:
            # Art. 9 quality requirements per ESAs Q&A and ESMA supervisory briefing
            art9_warnings = []

            if not dnsh_assessment:
                art9_warnings.append(
                    "Art. 9 QUALITY RISK: Do No Significant Harm (DNSH) assessment not performed. "
                    "All underlying investments must 'do no significant harm' to any sustainability "
                    "objective (SFDR Art. 2(17), Delegated Regulation (EU) 2022/1288 Art. 12)."
                )

            if not good_governance_checked:
                art9_warnings.append(
                    "Art. 9 QUALITY RISK: Good governance screening not applied to investee companies. "
                    "SFDR Art. 8(1) and Art. 9(1) both require investee companies to follow "
                    "good governance practices (sound management structures, employee relations, "
                    "remuneration, tax compliance)."
                )

            if min_sustainable_pct < _ART9_MIN_SUSTAINABLE_INVESTMENT:
                art9_warnings.append(
                    f"Art. 9 QUALITY RISK: Minimum sustainable investment commitment "
                    f"{min_sustainable_pct:.1f}% is below recommended 80%+ threshold. "
                    "ESMA expects Art. 9 funds to have all (or substantial majority) of "
                    "investments meeting SFDR Art. 2(17) sustainable investment definition. "
                    "Consider reclassification to Art. 8 if sustainable investments < 80%."
                )

            if art9_warnings:
                quality_warnings.extend(art9_warnings)

            # EU Paris-Aligned or Climate Transition benchmark triggers Art. 9 by default
            if benchmark_type == "eu_paris_aligned":
                classification = "9"
                disclosure_requirements.append(
                    "EU Paris-Aligned Benchmark used: fund automatically qualifies as Art. 9 "
                    "under SFDR Art. 9(3). Benchmark statement required in pre-contractual disclosures."
                )
            elif benchmark_type == "eu_climate_transition":
                classification = "9"
                disclosure_requirements.append(
                    "EU Climate Transition Benchmark used: Art. 9(3) applies. "
                    "Must explain how benchmark aligns with sustainable investment objective."
                )
            else:
                classification = "9"

            taxonomy_reporting_required = True
            pai_statement_required = True  # Art. 9 funds always include PAI in pre-contractual

            # Art. 9 disclosure requirements
            disclosure_requirements.extend([
                "SFDR Art. 10 + Delegated Reg. Annex III: Pre-contractual disclosure template "
                "(website, KIID/KID, fund prospectus) — minimum sustainable investment %, "
                "DNSH methodology, good governance assessment, benchmark alignment",
                "SFDR Art. 11: Periodic report disclosure — post-investment actual "
                "sustainable investment %, PAI impacts achieved, taxonomy alignment actual",
                "EU Taxonomy Art. 8 Delegated Act: Disclose % of investments in Taxonomy-aligned "
                f"economic activities (currently: {taxonomy_alignment_pct:.1f}%). "
                "Must separately disclose for Climate Mitigation, Adaptation, and other objectives.",
                "SFDR Art. 10 website disclosure: maintain product-level sustainability information "
                "on public website — updated at least annually",
                "PAI Statement: Mandatory for Art. 9. Report on all 14 mandatory + selected "
                "optional PAI indicators (Delegated Reg. Annex I, Table 1-2)",
                "Annual SFDR entity-level PAI statement with methodology and actions taken",
            ])

        # --- ARTICLE 8: Promotes Environmental or Social Characteristics ---
        elif promotes_esg:
            # Art. 8+ = Art. 8 fund with sustainable investment commitment
            if min_sustainable_pct >= _ART8_PLUS_MIN_SUSTAINABLE_PCT:
                classification = "8+"
                disclosure_requirements.append(
                    f"Article 8+ classification: fund promotes ESG characteristics AND commits "
                    f"minimum {min_sustainable_pct:.1f}% to sustainable investments (SFDR Art. 2(17)). "
                    "Disclose sustainable investment % separately from ESG-promoting investments."
                )
            else:
                classification = "8"

            taxonomy_reporting_required = True
            pai_statement_required = pai_considered  # Art. 8: PAI statement if considered

            # Check DNSH for Art. 8 with sustainable investment component
            if min_sustainable_pct > 0 and not dnsh_assessment:
                quality_warnings.append(
                    "Art. 8 QUALITY RISK: Fund commits to sustainable investments but "
                    "DNSH assessment not applied. DNSH is mandatory for any portion of "
                    "the portfolio classified as 'sustainable investment' under SFDR Art. 2(17)."
                )

            disclosure_requirements.extend([
                "SFDR Art. 8 + Delegated Reg. Annex II: Pre-contractual disclosure template — "
                "describe ESG characteristics promoted, binding elements of investment strategy, "
                f"minimum sustainable investment % ({min_sustainable_pct:.1f}%), "
                "exclusions applied, engagement policy",
                "SFDR Art. 11: Periodic report — actual attainment of ESG characteristics, "
                "taxonomy alignment (environmental investments), sustainable investment %",
                f"EU Taxonomy Art. 8: Disclose % taxonomy-aligned investments ({taxonomy_alignment_pct:.1f}%). "
                "Separate disclosure for principal adverse impact on taxonomy objectives.",
                "SFDR Art. 10 website disclosure: fund-level sustainability information",
                "ESG characteristics must be 'binding' — not aspirational. Constraints must be "
                "enforceable (exclusion lists, ESG scoring floors, engagement objectives with "
                "escalation mechanism). ESMA Supervisory Briefing on Sustainability (May 2023).",
            ])

            if not has_engagement_policy:
                disclosure_requirements.append(
                    "ADVISORY: Engagement policy not in place. Art. 8 funds are expected to "
                    "describe engagement/stewardship approach in pre-contractual disclosures "
                    "(SRD II Art. 3g; SFDR Delegated Reg. Annex II Q32)."
                )

            if pai_considered:
                disclosure_requirements.append(
                    "PAI Consideration: Disclose PAI indicators considered and how they "
                    "affect the ESG characteristics promoted (Delegated Reg. Art. 10, Q17)"
                )
            else:
                disclosure_requirements.append(
                    "PAI Not Considered: Include 'principal adverse impacts are not considered' "
                    "explanation in pre-contractual disclosure (Delegated Reg. Annex II Q17). "
                    "Explain why and when this may change."
                )

        # --- ARTICLE 6: No ESG Claims ---
        else:
            classification = "6"
            taxonomy_reporting_required = False
            pai_statement_required = False

            disclosure_requirements.extend([
                "SFDR Art. 6: Disclose how sustainability risks are integrated into investment "
                "decisions (or explain why not relevant to the strategy)",
                "SFDR Art. 6(2): If sustainability risks are deemed not relevant, explain clearly "
                "why — cannot simply state 'not applicable' without reasoning",
                "Art. 6 funds must NOT claim ESG credentials or use ESG-related names/labels "
                "(ESMA Guidelines on Fund Names using ESG/Sustainability-related terms, 2024)",
            ])

            if esg_integration:
                disclosure_requirements.append(
                    "ESG integration noted but insufficient for Art. 8 promotion: "
                    "ensure pre-contractual materials clearly state this is an Art. 6 fund "
                    "and do not imply ESG characteristics are promoted."
                )

        # =====================================================================
        # TAXONOMY REPORTING SPECIFICS
        # =====================================================================
        if taxonomy_reporting_required:
            disclosure_requirements.append(
                f"EU Taxonomy Disclosure (Art. 8 Taxonomy Regulation): "
                f"Current taxonomy alignment: {taxonomy_alignment_pct:.1f}%. "
                "Must disclose separately: (1) % aligned to Climate Mitigation objective, "
                "(2) % aligned to Climate Adaptation, (3) other environmental objectives. "
                "Non-taxonomy-aligned sustainable investments and other investments must "
                "be disclosed separately in the principal adverse impacts statement."
            )

        # =====================================================================
        # BENCHMARK-LINKED ADDITIONAL DISCLOSURES
        # =====================================================================
        if benchmark_type and benchmark_type not in {None, "none"}:
            disclosure_requirements.append(
                f"Benchmark disclosure: '{benchmark_type}' benchmark used. "
                "Explain in pre-contractual materials how the benchmark aligns with ESG "
                "characteristics or sustainable objective (SFDR Delegated Reg. Art. 14 / 15)."
            )

        # =====================================================================
        # ENTITY-LEVEL SFDR OBLIGATIONS (regardless of fund classification)
        # =====================================================================
        disclosure_requirements.append(
            "ENTITY-LEVEL SFDR Art. 3: Publish sustainability risk integration policy on website",
        )
        disclosure_requirements.append(
            "ENTITY-LEVEL SFDR Art. 4: Publish PAI statement OR explain why PAIs not considered "
            "(mandatory for entities with >500 employees from 30 June 2021)",
        )
        disclosure_requirements.append(
            "ENTITY-LEVEL SFDR Art. 5: Remuneration policy — describe how consistent with "
            "sustainability risks integration",
        )

        result = {
            "article_classification": classification,
            "fund_name": fund_name,
            "esg_integration": esg_integration,
            "promotes_esg": promotes_esg,
            "sustainable_objective": sustainable_objective,
            "taxonomy_alignment_pct": taxonomy_alignment_pct,
            "minimum_sustainable_investment_pct": min_sustainable_pct,
            "principal_adverse_impacts": pai_considered,
            "benchmark_type": benchmark_type,
            "dnsh_assessment": dnsh_assessment,
            "good_governance_checked": good_governance_checked,
            "taxonomy_reporting_required": taxonomy_reporting_required,
            "pai_statement_required": pai_statement_required,
            "disclosure_requirements": disclosure_requirements,
            "quality_warnings": quality_warnings,
            "classification_rationale": _get_classification_rationale(classification),
            "key_legislation": [
                "SFDR — Regulation (EU) 2019/2088 (Sustainable Finance Disclosure Regulation)",
                "SFDR Delegated Regulation (EU) 2022/1288 — Regulatory Technical Standards",
                "EU Taxonomy Regulation (EU) 2020/852",
                "ESMA Guidelines on Fund Names using ESG/Sustainability-related terms (2024)",
                "ESMA Supervisory Briefing — Sustainability Risks and Disclosures (May 2023)",
                "ESAs Joint Opinion on SFDR entity and product disclosures (September 2023)",
            ],
            "greenwashing_risk": (
                "HIGH" if (classification in {"8", "8+"} and not dnsh_assessment)
                else "MEDIUM" if (classification == "8" and min_sustainable_pct == 0)
                else "LOW"
            ),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"esg_sfdr_categorization failed: {e}")
        _log_lesson(f"esg_sfdr_categorization: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _get_classification_rationale(classification: str) -> str:
    """Return a plain-English rationale for the SFDR classification.

    Args:
        classification: SFDR article classification string.

    Returns:
        Human-readable rationale string.
    """
    rationales = {
        "6": (
            "Article 6: Fund does not promote ESG characteristics or have sustainable investment "
            "as its objective. Sustainability risks are considered (or reason for non-consideration "
            "disclosed) but no ESG claims are made."
        ),
        "8": (
            "Article 8: Fund promotes environmental or social characteristics using binding "
            "investment constraints. No minimum commitment to sustainable investments. "
            "Good governance is required for investee companies."
        ),
        "8+": (
            "Article 8+: Fund promotes ESG characteristics AND commits a minimum percentage "
            "of investments to sustainable investments as defined in SFDR Art. 2(17). "
            "DNSH assessment required for sustainable investment portion."
        ),
        "9": (
            "Article 9: Fund has sustainable investment as its primary objective. All investments "
            "must meet SFDR Art. 2(17) sustainable investment definition (except hedges and "
            "liquidity). DNSH, good governance, and PAI are all mandatory."
        ),
    }
    return rationales.get(classification, "Unknown classification")


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
