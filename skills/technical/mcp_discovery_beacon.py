"""
Executive Summary: Skill advertisement to the MCP network — formats skills as MCP-compatible payloads and estimates visibility score.
Inputs: skills_to_advertise (list of dicts: name str, description str, category str, price_ton float optional),
        beacon_interval_seconds (int, default 300)
Outputs: beacon_config (dict), advertisement_payloads (list), discovery_endpoint (str), visibility_score (float)
MCP Tool Name: mcp_discovery_beacon
"""
import os
import logging
import math
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

# Category weight table — higher-value categories boost visibility
CATEGORY_WEIGHTS: dict[str, float] = {
    "fund_accounting": 1.5,
    "trading":         1.4,
    "risk":            1.3,
    "analytics":       1.2,
    "tax":             1.2,
    "treasury":        1.3,
    "real_estate":     1.1,
    "credit":          1.1,
    "security":        1.0,
    "infrastructure":  0.9,
    "reporting":       1.0,
}

DEFAULT_CATEGORY_WEIGHT: float = 1.0

TOOL_META = {
    "name": "mcp_discovery_beacon",
    "description": (
        "Packages a list of Snowdrop skills into MCP-compatible advertisement payloads "
        "and generates the beacon configuration required for periodic self-registration "
        "on the MCP network. Calculates a visibility score (0–100) based on skill count "
        "and category diversity."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills_to_advertise": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name":        {"type": "string"},
                        "description": {"type": "string"},
                        "category":    {"type": "string"},
                        "price_ton":   {"type": "number", "description": "Price in TON tokens per call. Optional."},
                    },
                    "required": ["name", "description", "category"],
                },
            },
            "beacon_interval_seconds": {
                "type": "integer",
                "default": 300,
                "description": "How often the beacon re-registers with the MCP network (seconds).",
            },
        },
        "required": ["skills_to_advertise"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "beacon_config":          {"type": "object"},
            "advertisement_payloads": {"type": "array"},
            "discovery_endpoint":     {"type": "string"},
            "visibility_score":       {"type": "number"},
            "status":                 {"type": "string"},
            "timestamp":              {"type": "string"},
        },
        "required": [
            "beacon_config", "advertisement_payloads", "discovery_endpoint",
            "visibility_score", "status", "timestamp"
        ],
    },
}


def _compute_visibility_score(skills: list[dict[str, Any]]) -> float:
    """Compute MCP network visibility score (0–100) based on skill count and category mix.

    Formula:
        raw = sum(category_weight) * log2(skill_count + 1)
        normalised to 0–100 cap.

    Args:
        skills: List of skill descriptors with at least a "category" key.

    Returns:
        Visibility score between 0.0 and 100.0.
    """
    if not skills:
        return 0.0

    weight_sum: float = sum(
        CATEGORY_WEIGHTS.get(s.get("category", "").lower(), DEFAULT_CATEGORY_WEIGHT)
        for s in skills
    )
    unique_categories: int = len({s.get("category", "").lower() for s in skills})
    diversity_bonus: float = 1.0 + (unique_categories - 1) * 0.05  # 5% bonus per extra category

    raw_score: float = weight_sum * math.log2(len(skills) + 1) * diversity_bonus
    # Normalise: empirically cap at 100 (raw ~= 100 at ~25 premium skills)
    return round(min(raw_score * 4.0, 100.0), 2)


def mcp_discovery_beacon(
    skills_to_advertise: list[dict[str, Any]],
    beacon_interval_seconds: int = 300,
) -> dict[str, Any]:
    """Generate MCP skill advertisement payloads and beacon configuration.

    Each advertised skill becomes an MCP-compatible tool descriptor in the
    advertisement_payloads list. The beacon_config drives the periodic
    self-registration loop that keeps Snowdrop discoverable on the network.

    Args:
        skills_to_advertise: Skills to publish. Each dict must contain:
            - name (str): Unique skill identifier (snake_case).
            - description (str): What the skill does (1–2 sentences).
            - category (str): Skill category for routing and weighting.
            - price_ton (float, optional): Cost per call in TON tokens.
        beacon_interval_seconds (int): Re-registration frequency. Default 300 (5 min).

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - beacon_config (dict): Configuration for the beacon loop process.
            - advertisement_payloads (list[dict]): MCP tool descriptors per skill.
            - discovery_endpoint (str): Public URL for the agent card.
            - visibility_score (float): Estimated network visibility (0–100).
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        advertisement_payloads: list[dict[str, Any]] = []
        for skill in skills_to_advertise:
            skill_name: str = str(skill.get("name", "")).strip()
            description: str = str(skill.get("description", "")).strip()
            category: str = str(skill.get("category", "")).lower().strip()
            price_ton: float | None = (
                float(skill["price_ton"]) if "price_ton" in skill and skill["price_ton"] is not None else None
            )

            payload: dict[str, Any] = {
                "jsonrpc":  "2.0",
                "method":   "tools/register",
                "params": {
                    "tool": {
                        "name":        skill_name,
                        "description": description,
                        "category":    category,
                        "provider":    "snowdrop.stonewater.io",
                        "version":     "1.0.0",
                        "inputSchema":  {"type": "object", "properties": {}, "required": []},
                        "outputSchema": {"type": "object", "properties": {}, "required": []},
                        "pricing": {
                            "model":     "per_call",
                            "price_ton": price_ton,
                            "free_tier": price_ton is None,
                        },
                        "tags":        [category],
                        "advertised_at": now_utc.isoformat(),
                    }
                },
                "id": f"beacon-{skill_name}-{now_utc.timestamp():.0f}",
            }
            advertisement_payloads.append(payload)

        discovery_endpoint: str = "https://snowdrop.stonewater.io/.well-known/agent-card.json"

        beacon_config: dict[str, Any] = {
            "enabled":               True,
            "interval_seconds":      beacon_interval_seconds,
            "registration_endpoint": "https://mcp.network/tools/register",
            "discovery_endpoint":    discovery_endpoint,
            "skill_count":           len(skills_to_advertise),
            "last_beacon_at":        now_utc.isoformat(),
            "next_beacon_at":        (
                datetime.fromtimestamp(
                    now_utc.timestamp() + beacon_interval_seconds, tz=timezone.utc
                ).isoformat()
            ),
            "retry_policy": {
                "max_retries":        3,
                "backoff_seconds":    30,
            },
        }

        visibility_score: float = _compute_visibility_score(skills_to_advertise)

        return {
            "status":                 "success",
            "beacon_config":          beacon_config,
            "advertisement_payloads": advertisement_payloads,
            "discovery_endpoint":     discovery_endpoint,
            "visibility_score":       visibility_score,
            "timestamp":              now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"mcp_discovery_beacon failed: {e}")
        _log_lesson(f"mcp_discovery_beacon: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
