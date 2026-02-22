"""
Executive Summary: White-label Snowdrop intelligence skinning — generates branded portal config with filtered skill registry and rate limits.
Inputs: brand_config (dict: brand_name str, primary_color str, logo_url str,
        allowed_skills list[str], daily_limit_usd float), client_id (str)
Outputs: portal_config (dict), available_skills (list), rate_limit (dict), branding (dict)
MCP Tool Name: agentic_white_label_portal
"""
import os
import logging
import hashlib
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

# Master skill registry — all published Snowdrop skills and their categories
SKILL_REGISTRY: dict[str, dict[str, str]] = {
    "fund_nav_calculator":             {"category": "fund_accounting", "tier": "standard"},
    "capital_call_generator":          {"category": "fund_accounting", "tier": "standard"},
    "waterfall_distribution":          {"category": "fund_accounting", "tier": "premium"},
    "lp_statement_builder":            {"category": "fund_accounting", "tier": "standard"},
    "reit_dividend_reinvestment_logic": {"category": "real_estate",    "tier": "standard"},
    "venture_debt_amortization":       {"category": "credit",          "tier": "standard"},
    "global_tax_withholding_skill":    {"category": "tax",             "tier": "premium"},
    "financial_entity_graph":          {"category": "analytics",       "tier": "premium"},
    "portfolio_stress_test":           {"category": "risk",            "tier": "premium"},
    "latency_optimized_order_routing": {"category": "trading",         "tier": "enterprise"},
    "hardware_wallet_handshake":       {"category": "security",        "tier": "enterprise"},
    "api_key_rotation_logic":          {"category": "security",        "tier": "standard"},
    "agent_skill_version_checker":     {"category": "infrastructure",  "tier": "standard"},
    "sovereign_fiat_bridge":           {"category": "treasury",        "tier": "enterprise"},
    "transaction_sim_pre_flight":      {"category": "trading",         "tier": "enterprise"},
    "mcp_discovery_beacon":            {"category": "infrastructure",  "tier": "standard"},
    "agent_collaboration_handshake":   {"category": "infrastructure",  "tier": "premium"},
    "thunder_executive_briefing":      {"category": "reporting",       "tier": "standard"},
}

# Rate limit tiers (calls/day, max transaction size USD)
RATE_LIMIT_TIERS: dict[str, dict[str, Any]] = {
    "starter":    {"calls_per_day": 100,   "max_tx_usd": 10_000},
    "growth":     {"calls_per_day": 1_000,  "max_tx_usd": 100_000},
    "enterprise": {"calls_per_day": 10_000, "max_tx_usd": 10_000_000},
}

TOOL_META = {
    "name": "agentic_white_label_portal",
    "description": (
        "Generates a white-label portal configuration for a Snowdrop client. "
        "Filters the master skill registry to only those skills the client is "
        "authorised to access, applies branding overrides, assigns rate limits "
        "based on the daily USD transaction cap, and returns a complete portal "
        "configuration object ready for front-end consumption."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "brand_config": {
                "type": "object",
                "properties": {
                    "brand_name":     {"type": "string"},
                    "primary_color":  {"type": "string"},
                    "logo_url":       {"type": "string"},
                    "allowed_skills": {"type": "array", "items": {"type": "string"}},
                    "daily_limit_usd": {"type": "number"},
                },
                "required": ["brand_name", "primary_color", "logo_url", "allowed_skills", "daily_limit_usd"],
            },
            "client_id": {"type": "string"},
        },
        "required": ["brand_config", "client_id"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "portal_config":    {"type": "object"},
            "available_skills": {"type": "array"},
            "rate_limit":       {"type": "object"},
            "branding":         {"type": "object"},
            "status":           {"type": "string"},
            "timestamp":        {"type": "string"},
        },
        "required": ["portal_config", "available_skills", "rate_limit", "branding", "status", "timestamp"],
    },
}


def _assign_rate_limit_tier(daily_limit_usd: float) -> str:
    """Determine the rate limit tier based on the daily USD transaction cap.

    Args:
        daily_limit_usd: Maximum USD transacted per day.

    Returns:
        Tier name: "starter", "growth", or "enterprise".
    """
    if daily_limit_usd <= 10_000:
        return "starter"
    if daily_limit_usd <= 100_000:
        return "growth"
    return "enterprise"


def agentic_white_label_portal(
    brand_config: dict[str, Any],
    client_id: str,
) -> dict[str, Any]:
    """Generate a white-label portal configuration for a Snowdrop client.

    Args:
        brand_config: Branding and access configuration with keys:
            - brand_name (str): Client's brand name shown in the portal.
            - primary_color (str): Hex or CSS colour string (e.g. "#1A73E8").
            - logo_url (str): URL to the client's logo asset.
            - allowed_skills (list[str]): Skill names the client may access.
            - daily_limit_usd (float): Maximum daily transaction value in USD.
        client_id (str): Unique client identifier used for configuration scoping.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - portal_config (dict): Complete portal configuration object.
            - available_skills (list[dict]): Filtered skill descriptors.
            - rate_limit (dict): Assigned rate limits and tier name.
            - branding (dict): Validated branding settings.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        brand_name: str = str(brand_config.get("brand_name", "")).strip()
        primary_color: str = str(brand_config.get("primary_color", "#000000")).strip()
        logo_url: str = str(brand_config.get("logo_url", "")).strip()
        allowed_skills: list[str] = [s.lower() for s in brand_config.get("allowed_skills", [])]
        daily_limit_usd: float = float(brand_config.get("daily_limit_usd", 0.0))

        if not brand_name:
            raise ValueError("brand_name cannot be empty.")
        if not client_id:
            raise ValueError("client_id cannot be empty.")

        # Filter skill registry to allowed skills only
        available_skills: list[dict[str, Any]] = []
        for skill_name in allowed_skills:
            if skill_name in SKILL_REGISTRY:
                meta: dict[str, str] = SKILL_REGISTRY[skill_name]
                available_skills.append(
                    {
                        "name":     skill_name,
                        "category": meta["category"],
                        "tier":     meta["tier"],
                    }
                )
            else:
                logger.warning(f"agentic_white_label_portal: skill '{skill_name}' not in registry — skipped.")

        # Rate limit assignment
        tier_name: str = _assign_rate_limit_tier(daily_limit_usd)
        tier_config: dict[str, Any] = RATE_LIMIT_TIERS[tier_name]
        rate_limit: dict[str, Any] = {
            "tier":           tier_name,
            "calls_per_day":  tier_config["calls_per_day"],
            "max_tx_usd":     min(daily_limit_usd, tier_config["max_tx_usd"]),
            "daily_limit_usd": daily_limit_usd,
        }

        # Generate a deterministic portal ID
        portal_id: str = hashlib.sha256(
            f"{client_id}:{brand_name}:{now_utc.date().isoformat()}".encode()
        ).hexdigest()[:16]

        branding: dict[str, Any] = {
            "brand_name":    brand_name,
            "primary_color": primary_color,
            "logo_url":      logo_url,
        }

        portal_config: dict[str, Any] = {
            "portal_id":          portal_id,
            "client_id":          client_id,
            "branding":           branding,
            "skill_count":        len(available_skills),
            "rate_limit":         rate_limit,
            "generated_at":       now_utc.isoformat(),
            "powered_by":         "Snowdrop by Stonewater Solutions LLC",
            "mcp_endpoint":       f"/mcp/{client_id}/tools",
            "discovery_endpoint": f"/.well-known/agent-card.json?client={client_id}",
        }

        return {
            "status":           "success",
            "portal_config":    portal_config,
            "available_skills": available_skills,
            "rate_limit":       rate_limit,
            "branding":         branding,
            "timestamp":        now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"agentic_white_label_portal failed: {e}")
        _log_lesson(f"agentic_white_label_portal: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
