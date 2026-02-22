"""
Executive Summary: EU MiCA token categorization — classifies crypto-assets as ART, EMT, or Utility Token per MiCA Regulation (EU) 2023/1114.
Inputs: token_data (dict: name, issuer, backing_type, is_stablecoin, market_cap_eur, daily_volume_eur)
Outputs: classification (str), significant (bool), requirements (list), citations (list)
MCP Tool Name: mica_asset_classification
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "mica_asset_classification",
    "description": (
        "Classifies crypto-assets under EU MiCA Regulation (EU) 2023/1114 as ART "
        "(Asset-Referenced Token), EMT (E-Money Token), or Utility Token. Flags "
        "significant status based on market cap and daily volume thresholds."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "token_data": {
                "type": "object",
                "description": "Token metadata for MiCA classification",
                "properties": {
                    "name": {"type": "string"},
                    "issuer": {"type": "string"},
                    "backing_type": {
                        "type": "string",
                        "enum": ["fiat", "crypto", "algorithmic", "commodity", "basket", "none"],
                    },
                    "is_stablecoin": {"type": "boolean"},
                    "market_cap_eur": {"type": "number"},
                    "daily_volume_eur": {"type": "number"},
                },
                "required": ["name", "issuer", "backing_type", "is_stablecoin", "market_cap_eur", "daily_volume_eur"],
            }
        },
        "required": ["token_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "classification": {"type": "string"},
            "significant": {"type": "boolean"},
            "requirements": {"type": "array", "items": {"type": "string"}},
            "citations": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["classification", "significant", "requirements", "citations", "status", "timestamp"],
    },
}

# MiCA significance thresholds (Article 43 / Article 56)
_SIGNIFICANT_MARKET_CAP_EUR = 5_000_000_000   # 5 billion EUR
_SIGNIFICANT_DAILY_VOLUME_EUR = 500_000_000    # 500 million EUR


def mica_asset_classification(token_data: dict[str, Any]) -> dict[str, Any]:
    """Classify a crypto-asset under EU MiCA Regulation (EU) 2023/1114.

    Determines whether the token is an Asset-Referenced Token (ART),
    E-Money Token (EMT), or Utility Token, then checks significance
    thresholds per Article 43 (ART) and Article 56 (EMT).

    Args:
        token_data: Dictionary containing token metadata including name,
            issuer, backing_type, is_stablecoin, market_cap_eur, and
            daily_volume_eur.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            classification (str): "ART", "EMT", "Utility Token", or
                "Other Crypto-Asset".
            significant (bool): True if thresholds breached.
            requirements (list[str]): Regulatory obligations for this class.
            citations (list[str]): Relevant MiCA article references.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        name: str = token_data.get("name", "")
        issuer: str = token_data.get("issuer", "")
        backing_type: str = str(token_data.get("backing_type", "none")).lower()
        is_stablecoin: bool = bool(token_data.get("is_stablecoin", False))
        market_cap_eur: float = float(token_data.get("market_cap_eur", 0))
        daily_volume_eur: float = float(token_data.get("daily_volume_eur", 0))

        # --- Classification logic ---
        # EMT: pegged to a single fiat currency (MiCA Title IV, Articles 48-58)
        if is_stablecoin and backing_type == "fiat":
            classification = "EMT"
            citations = [
                "MiCA Art. 48 — Definition of e-money token",
                "MiCA Art. 49 — Issuance of e-money tokens",
                "MiCA Art. 50 — Obligations of issuers of e-money tokens",
                "MiCA Art. 54 — Redemption rights",
                "MiCA Art. 56 — Significant e-money tokens",
            ]
            requirements = [
                "Must be issued by a credit institution or electronic money institution (Art. 48)",
                "Whitepaper required and notified to NCA (Art. 51)",
                "Funds must be invested in secure low-risk assets (Art. 53)",
                "Holders have permanent redemption right at par value (Art. 54)",
                "Reserve assets must be segregated and protected in insolvency (Art. 53(4))",
                "Quarterly reports on reserve composition to NCA (Art. 55)",
            ]
            significant = (
                market_cap_eur > _SIGNIFICANT_MARKET_CAP_EUR
                or daily_volume_eur > _SIGNIFICANT_DAILY_VOLUME_EUR
            )
            if significant:
                requirements += [
                    "EBA direct supervision applies (Art. 56)",
                    "Enhanced liquidity management policy required (Art. 45 by reference)",
                    "Interoperability obligations with payment systems (Art. 57)",
                    "Cap on issuance may be imposed by EBA (Art. 58)",
                ]
                citations.append("MiCA Art. 57 — Significant EMT interoperability obligations")
                citations.append("MiCA Art. 58 — Caps on significant EMTs")

        # ART: referenced to multiple currencies, commodities, crypto, or baskets
        # (MiCA Title III, Articles 16-47)
        elif is_stablecoin and backing_type in {"crypto", "commodity", "basket"}:
            classification = "ART"
            citations = [
                "MiCA Art. 3(1)(6) — Definition of asset-referenced token",
                "MiCA Art. 16 — Authorisation to offer ARTs",
                "MiCA Art. 17 — Content of whitepaper for ARTs",
                "MiCA Art. 36 — Reserve of assets",
                "MiCA Art. 43 — Significant asset-referenced tokens",
            ]
            requirements = [
                "Authorisation from NCA required unless exempt (Art. 16)",
                "Crypto-asset whitepaper approved by NCA before issuance (Art. 17)",
                "Reserve of assets matching references at all times (Art. 36)",
                "Custody of reserve assets with qualified custodian (Art. 37)",
                "At least 30% of reserve in deposits at credit institutions (Art. 38)",
                "Quarterly reserve attestation by independent auditor (Art. 22)",
                "Governance and risk management framework (Arts. 34-35)",
                "Marketing materials approved by NCA (Art. 25)",
            ]
            significant = (
                market_cap_eur > _SIGNIFICANT_MARKET_CAP_EUR
                or daily_volume_eur > _SIGNIFICANT_DAILY_VOLUME_EUR
            )
            if significant:
                requirements += [
                    "EBA assumes supervisory lead alongside NCA (Art. 43)",
                    "Liquidity stress testing at least semi-annually (Art. 45)",
                    "Recovery and redemption plan (Art. 46)",
                    "Mandatory supervisory college (Art. 44)",
                ]
                citations.append("MiCA Art. 44 — Supervisory college for significant ARTs")
                citations.append("MiCA Art. 45 — Additional obligations for significant ARTs")

        # Algorithmic stablecoin — MiCA bans fully algorithmic no-reserve stablecoins
        elif is_stablecoin and backing_type == "algorithmic":
            classification = "ART"  # Treated as ART but with prohibition risk
            significant = (
                market_cap_eur > _SIGNIFICANT_MARKET_CAP_EUR
                or daily_volume_eur > _SIGNIFICANT_DAILY_VOLUME_EUR
            )
            requirements = [
                "WARNING: Purely algorithmic stablecoins with no reserve are PROHIBITED under MiCA (Art. 68(2))",
                "Tokens that purport to maintain a stable value through algorithms without reserve assets cannot be issued",
                "If partial reserve exists, classify under ART rules and seek NCA guidance",
                "Legal opinion recommended before any EU offering",
            ]
            citations = [
                "MiCA Art. 68(2) — Prohibition on algorithmic stablecoins without reserve",
                "MiCA Recital 66 — Rationale for algorithmic stablecoin prohibition",
            ]

        # Utility token: no stability mechanism, used to access a service
        elif not is_stablecoin and backing_type == "none":
            classification = "Utility Token"
            significant = False  # Significance thresholds only apply to ART/EMT
            citations = [
                "MiCA Art. 3(1)(9) — Definition of utility token",
                "MiCA Art. 4 — Whitepaper requirements for utility tokens",
                "MiCA Art. 5 — Content and form of crypto-asset whitepaper",
                "MiCA Art. 9 — Liability for whitepaper",
            ]
            requirements = [
                "Crypto-asset whitepaper required if offered to public (Art. 4)",
                "Whitepaper must be notified to NCA before publication (Art. 8)",
                "Right of withdrawal for retail investors: 14 days (Art. 13)",
                "Marketing communications must be fair and clear (Art. 7)",
                "No authorisation required but NCA notification mandatory (Art. 8)",
                "Liability for misleading whitepaper falls on issuer (Art. 9)",
            ]

        # Catch-all for crypto-assets not fitting above categories (e.g., NFTs, DeFi tokens)
        else:
            classification = "Other Crypto-Asset"
            significant = False
            citations = [
                "MiCA Art. 2 — Scope of MiCA",
                "MiCA Art. 3 — Definitions",
                "MiCA Recital 11 — Exclusions from MiCA scope",
            ]
            requirements = [
                "Review whether token is excluded from MiCA scope (Art. 2(4))",
                "NFTs may be excluded unless issued in large fungible series",
                "DeFi protocols may be excluded if fully decentralised (Recital 22)",
                "Seek NCA guidance or legal opinion for borderline cases",
                "Whitepaper may still be required if offered publicly",
            ]

        result = {
            "classification": classification,
            "token_name": name,
            "issuer": issuer,
            "significant": significant,
            "market_cap_eur": market_cap_eur,
            "daily_volume_eur": daily_volume_eur,
            "significance_thresholds": {
                "market_cap_eur": _SIGNIFICANT_MARKET_CAP_EUR,
                "daily_volume_eur": _SIGNIFICANT_DAILY_VOLUME_EUR,
            },
            "requirements": requirements,
            "citations": citations,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"mica_asset_classification failed: {e}")
        _log_lesson(f"mica_asset_classification: {e}")
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
        pass  # Do not raise inside error handler
