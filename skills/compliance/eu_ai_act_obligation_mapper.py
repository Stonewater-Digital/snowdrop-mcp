"""Map EU AI Act obligations by role and risk class."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence

TOOL_META: dict[str, Any] = {
    "name": "eu_ai_act_obligation_mapper",
    "description": (
        "Returns EU AI Act obligations for a specified actor role and AI system risk "
        "class. Accepts optional deployment stage and use-case context to prioritize "
        "relevant controls."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "role": {
                "type": "string",
                "description": "Economic actor role under the EU AI Act (e.g., provider, deployer).",
            },
            "system_type": {
                "type": "string",
                "description": (
                    "Primary system risk class (e.g., high_risk_annex_III, general_purpose, "
                    "limited_risk). Provide this or system_types."
                ),
            },
            "system_types": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional list of risk classes if multiple apply.",
            },
            "deployment_stage": {
                "type": "string",
                "enum": ["pre_market", "post_market", "monitoring", "incident"],
                "description": "Focus phase to filter obligations.",
            },
            "use_case": {
                "type": "string",
                "description": "Free text describing the use-case for keyword matching.",
            },
            "detail_level": {
                "type": "string",
                "enum": ["summary", "full"],
                "default": "summary",
                "description": "Set to 'full' to include deliverables/evidence lists.",
            },
        },
        "required": ["role"],
        "anyOf": [
            {"required": ["system_type"]},
            {"required": ["system_types"]},
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}

BASE_DIR = Path(__file__).resolve().parents[2]
REFERENCE_PATH = BASE_DIR / "state" / "eu_ai_act_obligations.json"
LOG_PATH = BASE_DIR / "logs" / "lessons.md"

ROLE_ALIASES: dict[str, set[str]] = {
    "provider": {"provider", "ai_provider", "builder", "manufacturer"},
    "deployer": {"deployer", "user", "operator"},
    "importer": {"importer"},
    "distributor": {"distributor"},
    "authorized_representative": {"authorized_representative", "authorised_representative"},
    "product_manufacturer": {"product_manufacturer"},
    "general_purpose_provider": {"general_purpose_provider", "gpai_provider"},
    "general_purpose_integrator": {"general_purpose_integrator", "integrator"},
}

SYSTEM_ALIASES: dict[str, set[str]] = {
    "high_risk_annex_i": {"high_risk_annex_i", "annex_i", "product_high_risk"},
    "high_risk_annex_iii": {"high_risk_annex_iii", "annex_iii", "high_risk"},
    "limited_risk": {"limited_risk", "transparency", "art_52"},
    "general_purpose": {"general_purpose", "gpai", "foundation_model"},
    "general_purpose_integrated": {"general_purpose_integrated", "gpai_integrated", "downstream"},
    "minimal_risk": {"minimal_risk", "none"},
}

ALLOWED_DETAIL_LEVELS = {"summary", "full"}
ALLOWED_DEPLOYMENT_STAGES = {"pre_market", "post_market", "monitoring", "incident"}


@lru_cache(maxsize=1)
def _load_reference() -> dict[str, Any]:
    with REFERENCE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _normalize_role(role: str) -> str:
    candidate = role.strip().lower()
    for canonical, synonyms in ROLE_ALIASES.items():
        if candidate == canonical or candidate in synonyms:
            return canonical
    raise ValueError(
        "Unsupported role. Provide one of: " + ", ".join(sorted(ROLE_ALIASES))
    )


def _normalize_system_types(
    system_type: str | None, system_types: Sequence[str] | None
) -> list[str]:
    provided: list[str] = []
    if system_type:
        provided.append(system_type)
    if system_types:
        provided.extend(system_types)
    if not provided:
        raise ValueError("system_type or system_types must be supplied")
    normalized: list[str] = []
    for raw_value in provided:
        candidate = raw_value.strip().lower()
        matched = None
        for canonical, aliases in SYSTEM_ALIASES.items():
            if candidate == canonical or candidate in aliases:
                matched = canonical
                break
        if not matched:
            raise ValueError(
                "Unsupported system type. Provide one of: "
                + ", ".join(sorted(SYSTEM_ALIASES))
            )
        normalized.append(matched)
    return sorted(set(normalized))


def _keyword_hits(keywords: Iterable[str], use_case: str | None) -> list[str]:
    if not use_case:
        return []
    text = use_case.lower()
    return [kw for kw in keywords if kw.lower() in text]


def _format_obligation(entry: dict[str, Any], detail_level: str) -> dict[str, Any]:
    base = {
        "id": entry["id"],
        "title": entry["title"],
        "summary": entry["summary"],
        "articles": entry["articles"],
        "roles": entry["roles"],
        "risk_classes": entry["risk_classes"],
        "priority": entry.get("priority", "mandatory"),
        "deadline": entry.get("deadline"),
        "detail_level": detail_level,
    }
    if detail_level == "full":
        base["actions"] = entry.get("actions", [])
        base["deliverables"] = entry.get("deliverables", [])
        base["evidence"] = entry.get("evidence", [])
    return base


def eu_ai_act_obligation_mapper(
    role: str,
    system_type: str | None = None,
    system_types: Sequence[str] | None = None,
    use_case: str | None = None,
    deployment_stage: str | None = None,
    detail_level: str = "summary",
    **_: Any,
) -> dict[str, Any]:
    """Return the matching obligation bundle."""

    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        normalized_role = _normalize_role(role)
        normalized_systems = _normalize_system_types(system_type, system_types)
        if deployment_stage and deployment_stage not in ALLOWED_DEPLOYMENT_STAGES:
            raise ValueError(
                "deployment_stage must be one of " + ", ".join(sorted(ALLOWED_DEPLOYMENT_STAGES))
            )
        normalized_stage = deployment_stage
        normalized_detail = detail_level.lower().strip()
        if normalized_detail not in ALLOWED_DETAIL_LEVELS:
            raise ValueError("detail_level must be 'summary' or 'full'")

        reference = _load_reference()
        obligations = reference.get("obligations", [])
        matches: list[dict[str, Any]] = []
        for entry in obligations:
            if normalized_role not in entry.get("roles", []):
                continue
            if not set(normalized_systems) & set(entry.get("risk_classes", [])):
                continue
            if normalized_stage and normalized_stage not in entry.get(
                "deployment_phases", ALLOWED_DEPLOYMENT_STAGES
            ):
                continue

            reasons: list[str] = []
            score = 0.0
            overlap = set(normalized_systems) & set(entry.get("risk_classes", []))
            if overlap:
                score += 2
                reasons.append("risk_class match: " + ", ".join(sorted(overlap)))
            if normalized_stage and normalized_stage in entry.get(
                "deployment_phases", []
            ):
                score += 1
                reasons.append(f"deployment_stage match: {normalized_stage}")
            hits = _keyword_hits(entry.get("keywords", []), use_case)
            if hits:
                score += 1 + 0.1 * len(hits)
                reasons.append("keyword match: " + ", ".join(hits))

            formatted = _format_obligation(entry, normalized_detail)
            formatted["match_reasons"] = reasons
            formatted["match_score"] = round(score, 2)
            matches.append(formatted)

        matches.sort(key=lambda item: item["match_score"], reverse=True)

        coverage_note = ""
        if not matches:
            coverage_note = (
                "No obligations triggered for the given combination. Confirm the role/risk "
                "class or update the reference data."
            )

        return {
            "status": "success",
            "data": {
                "role": normalized_role,
                "system_types": normalized_systems,
                "deployment_stage": normalized_stage,
                "detail_level": normalized_detail,
                "matched_obligations": matches,
                "coverage_note": coverage_note,
                "reference_version": reference.get("metadata", {}).get("version"),
            },
            "timestamp": timestamp,
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("eu_ai_act_obligation_mapper", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": timestamp,
        }


def _log_lesson(skill_name: str, message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {message}\n")
