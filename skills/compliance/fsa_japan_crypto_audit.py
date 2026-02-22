"""
Executive Summary: Japanese FSA crypto-asset exchange compliance audit — verifies cold storage ratios, asset segregation, and proprietary/customer asset separation per Payment Services Act requirements.
Inputs: exchange_data (dict: total_customer_assets, cold_storage_pct, hot_wallet_pct, segregation_method, audit_date)
Outputs: compliant (bool), findings (list), cold_storage_ratio (float), recommendations (list)
MCP Tool Name: fsa_japan_crypto_audit
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fsa_japan_crypto_audit",
    "description": (
        "Audits a Japanese crypto-asset exchange against FSA (Financial Services Agency) "
        "requirements under the Payment Services Act (資金決済に関する法律), specifically "
        "cold storage minimums, asset segregation, and operational security controls."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "exchange_data": {
                "type": "object",
                "properties": {
                    "total_customer_assets": {
                        "type": "number",
                        "description": "Total value of customer crypto-assets in JPY",
                    },
                    "cold_storage_pct": {
                        "type": "number",
                        "description": "Percentage of customer assets held in cold storage (0-100)",
                    },
                    "hot_wallet_pct": {
                        "type": "number",
                        "description": "Percentage of customer assets held in hot wallets (0-100)",
                    },
                    "segregation_method": {
                        "type": "string",
                        "description": "Method of asset segregation: separate_wallets / separate_accounts / trust / none",
                    },
                    "audit_date": {
                        "type": "string",
                        "description": "ISO-8601 date of the audit (YYYY-MM-DD)",
                    },
                    "proprietary_assets_commingled": {
                        "type": "boolean",
                        "description": "Whether proprietary assets are mixed with customer assets",
                    },
                    "insurance_coverage_jpy": {
                        "type": "number",
                        "description": "Value of cyber insurance coverage in JPY",
                    },
                    "multi_sig_required": {
                        "type": "boolean",
                        "description": "Whether multi-signature authorisation is required for withdrawals",
                    },
                    "annual_security_audit": {
                        "type": "boolean",
                        "description": "Whether an independent annual security audit has been conducted",
                    },
                    "registered_with_fsa": {
                        "type": "boolean",
                        "description": "Whether the exchange holds a valid FSA CAESP registration",
                    },
                },
                "required": [
                    "total_customer_assets",
                    "cold_storage_pct",
                    "hot_wallet_pct",
                    "segregation_method",
                    "audit_date",
                ],
            }
        },
        "required": ["exchange_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "compliant": {"type": "boolean"},
            "findings": {"type": "array", "items": {"type": "string"}},
            "cold_storage_ratio": {"type": "number"},
            "recommendations": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["compliant", "findings", "cold_storage_ratio", "recommendations", "status", "timestamp"],
    },
}

# FSA thresholds (Payment Services Act, Cabinet Office Ordinance on CAESP)
_MIN_COLD_STORAGE_PCT = 95.0        # 95% or more must be in cold storage
_MAX_HOT_WALLET_PCT = 5.0           # Hot wallet limited to 5%
_HOT_WALLET_INSURANCE_RATIO = 1.0  # Hot wallet value must be fully covered by insurance


def fsa_japan_crypto_audit(exchange_data: dict[str, Any]) -> dict[str, Any]:
    """Audit a crypto-asset exchange against Japanese FSA requirements.

    Checks cold storage percentage against the 95% minimum, verifies
    asset segregation from proprietary funds, and reviews operational
    security controls required under the Payment Services Act and the
    Cabinet Office Ordinance on Crypto-Asset Exchange Service Providers (CAESP).

    Args:
        exchange_data: Dictionary with exchange operational data including
            storage allocation, segregation method, insurance, and audit status.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            compliant (bool): Overall FSA compliance status.
            findings (list[str]): Specific rule breaches or concerns.
            cold_storage_ratio (float): Actual cold storage percentage (0-100).
            recommendations (list[str]): Remediation steps.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        total_customer_assets: float = float(exchange_data.get("total_customer_assets", 0))
        cold_storage_pct: float = float(exchange_data.get("cold_storage_pct", 0))
        hot_wallet_pct: float = float(exchange_data.get("hot_wallet_pct", 0))
        segregation_method: str = str(exchange_data.get("segregation_method", "none")).lower()
        audit_date_str: str = str(exchange_data.get("audit_date", ""))
        proprietary_commingled: bool = bool(exchange_data.get("proprietary_assets_commingled", False))
        insurance_coverage_jpy: float = float(exchange_data.get("insurance_coverage_jpy", 0))
        multi_sig_required: bool = bool(exchange_data.get("multi_sig_required", False))
        annual_security_audit: bool = bool(exchange_data.get("annual_security_audit", False))
        registered_with_fsa: bool = bool(exchange_data.get("registered_with_fsa", False))

        findings: list[str] = []
        recommendations: list[str] = []

        # --- FSA Registration ---
        if not registered_with_fsa:
            findings.append(
                "CRITICAL: Exchange is not registered as a Crypto-Asset Exchange Service Provider (CAESP) "
                "with the FSA — operation without registration is a criminal offence under "
                "Payment Services Act Article 63-2"
            )
            recommendations.append(
                "Immediately cease operations and apply for FSA CAESP registration or "
                "obtain a licence from a registered provider"
            )

        # --- Cold Storage Requirement ---
        # Payment Services Act Article 63-11; Cabinet Office Ordinance Article 20
        if cold_storage_pct < _MIN_COLD_STORAGE_PCT:
            shortage = _MIN_COLD_STORAGE_PCT - cold_storage_pct
            findings.append(
                f"Cold storage ratio {cold_storage_pct:.2f}% is below the 95% FSA minimum "
                f"(Payment Services Act Art. 63-11; Cabinet Office Ordinance Art. 20). "
                f"Shortfall: {shortage:.2f} percentage points."
            )
            recommendations.append(
                f"Transfer at least {shortage:.2f}% of customer assets from hot wallets to "
                "air-gapped cold storage. Target ≥95% cold storage compliance."
            )
        else:
            findings.append(
                f"Cold storage ratio {cold_storage_pct:.2f}% meets the 95% FSA minimum — PASS"
            )

        # --- Hot Wallet Cap ---
        if hot_wallet_pct > _MAX_HOT_WALLET_PCT:
            findings.append(
                f"Hot wallet exposure {hot_wallet_pct:.2f}% exceeds the 5% ceiling. "
                "Hot wallet assets must be fully covered by cyber insurance."
            )

        # --- Hot Wallet Insurance Coverage ---
        if hot_wallet_pct > 0 and total_customer_assets > 0:
            hot_wallet_value_jpy = (hot_wallet_pct / 100) * total_customer_assets
            if insurance_coverage_jpy < hot_wallet_value_jpy:
                insurance_gap = hot_wallet_value_jpy - insurance_coverage_jpy
                findings.append(
                    f"Cyber insurance coverage ¥{insurance_coverage_jpy:,.0f} is insufficient to "
                    f"cover hot wallet value ¥{hot_wallet_value_jpy:,.0f} "
                    f"(gap: ¥{insurance_gap:,.0f}). FSA requires hot wallet assets to be "
                    "fully insured (Cabinet Office Ordinance Art. 20(2))."
                )
                recommendations.append(
                    f"Increase cyber insurance coverage by at least ¥{insurance_gap:,.0f} to "
                    "match total hot wallet asset value."
                )

        # --- Asset Segregation ---
        # Payment Services Act Article 63-11-2: strict segregation of customer and proprietary assets
        _APPROVED_SEGREGATION_METHODS = {"separate_wallets", "trust"}
        if segregation_method not in _APPROVED_SEGREGATION_METHODS:
            findings.append(
                f"Segregation method '{segregation_method}' is not an FSA-approved method. "
                "FSA requires physically separate wallet addresses or a trust arrangement "
                "(Payment Services Act Art. 63-11-2)."
            )
            recommendations.append(
                "Implement wallet-level segregation: unique wallet clusters per customer "
                "or a third-party trust arrangement with an FSA-registered trust bank."
            )
        else:
            findings.append(
                f"Asset segregation method '{segregation_method}' is FSA-compliant — PASS"
            )

        if proprietary_commingled:
            findings.append(
                "CRITICAL: Proprietary exchange assets are commingled with customer assets — "
                "this directly violates Payment Services Act Article 63-11-2 and constitutes "
                "a basis for licence revocation."
            )
            recommendations.append(
                "Immediately separate all proprietary exchange assets into distinct wallets/accounts "
                "with no shared keys or addresses with customer funds."
            )

        # --- Multi-Signature Control ---
        # FSA expects multi-sig for cold storage withdrawals (NDA 2023 guidance)
        if not multi_sig_required:
            findings.append(
                "Multi-signature authentication is not required for fund withdrawals. "
                "FSA guidance (2023 cybersecurity requirements) expects multi-sig controls "
                "on all cold storage wallet operations."
            )
            recommendations.append(
                "Implement M-of-N multi-signature scheme (minimum 2-of-3) for all "
                "cold storage withdrawal authorisations."
            )
        else:
            findings.append("Multi-signature withdrawal controls in place — PASS")

        # --- Annual Security Audit ---
        if not annual_security_audit:
            findings.append(
                "No independent annual security audit on record. "
                "FSA cybersecurity guidelines require annual third-party penetration testing "
                "and systems audit."
            )
            recommendations.append(
                "Engage an FSA-recognised information security firm to conduct a "
                "full penetration test and systems security audit annually."
            )
        else:
            findings.append("Annual independent security audit completed — PASS")

        # --- Reporting Cycle Check ---
        # Monthly self-assessment report (Cabinet Office Ordinance Art. 25)
        recommendations.append(
            "Submit monthly self-assessment report to FSA per Cabinet Office Ordinance Article 25"
        )
        recommendations.append(
            "File annual business report within 3 months of fiscal year end (PSA Art. 63-22)"
        )

        # --- Overall Compliance ---
        critical_findings = [f for f in findings if "CRITICAL" in f]
        compliant = (
            cold_storage_pct >= _MIN_COLD_STORAGE_PCT
            and segregation_method in _APPROVED_SEGREGATION_METHODS
            and not proprietary_commingled
            and registered_with_fsa
            and len(critical_findings) == 0
        )

        result = {
            "compliant": compliant,
            "registered_with_fsa": registered_with_fsa,
            "cold_storage_ratio": cold_storage_pct,
            "hot_wallet_ratio": hot_wallet_pct,
            "fsa_cold_storage_minimum_pct": _MIN_COLD_STORAGE_PCT,
            "segregation_method": segregation_method,
            "proprietary_assets_commingled": proprietary_commingled,
            "total_customer_assets_jpy": total_customer_assets,
            "insurance_coverage_jpy": insurance_coverage_jpy,
            "multi_sig_required": multi_sig_required,
            "annual_security_audit": annual_security_audit,
            "critical_finding_count": len(critical_findings),
            "findings": findings,
            "recommendations": recommendations,
            "regulations_checked": [
                "Payment Services Act (資金決済に関する法律) Art. 63-2, 63-11, 63-11-2, 63-22",
                "Cabinet Office Ordinance on CAESP — Art. 20, 25",
                "FSA Cybersecurity Guidelines for CAESP (2023)",
                "FSA Guidelines on Customer Asset Management (2020 revision)",
            ],
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"fsa_japan_crypto_audit failed: {e}")
        _log_lesson(f"fsa_japan_crypto_audit: {e}")
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
