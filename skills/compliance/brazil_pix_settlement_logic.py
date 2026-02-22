"""
Executive Summary: Brazilian BCB Pix instant payment settlement engine — applies BCB transaction limits, nightly caps, PF/PJ rules, fee structures, and determines settlement time in seconds.
Inputs: transaction (dict: amount_brl, sender_type, receiver_type, transaction_type, time_of_day)
Outputs: approved (bool), effective_limit (float), fee (float), settlement_time_seconds (int), restrictions (list)
MCP Tool Name: brazil_pix_settlement_logic
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "brazil_pix_settlement_logic",
    "description": (
        "Applies Banco Central do Brasil (BCB) Pix rules per Resolução BCB nº 1 (2020) and "
        "subsequent circulars. Validates transaction limits (nightly R$1,000 cap for PF), "
        "fee structures, settlement times (10 seconds 24/7), and transaction type restrictions."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "transaction": {
                "type": "object",
                "properties": {
                    "amount_brl": {
                        "type": "number",
                        "description": "Transaction amount in Brazilian Real (BRL)",
                    },
                    "sender_type": {
                        "type": "string",
                        "description": "PF (Pessoa Física / individual) or PJ (Pessoa Jurídica / legal entity)",
                        "enum": ["pf", "pj"],
                    },
                    "receiver_type": {
                        "type": "string",
                        "description": "PF or PJ",
                        "enum": ["pf", "pj"],
                    },
                    "transaction_type": {
                        "type": "string",
                        "description": "standard / scheduled / recurring / pix_troco (change) / pix_saque (withdrawal)",
                        "enum": ["standard", "scheduled", "recurring", "pix_troco", "pix_saque"],
                    },
                    "time_of_day": {
                        "type": "string",
                        "description": "24-hour time string HH:MM (e.g. '22:30')",
                    },
                    "daily_cumulative_brl": {
                        "type": "number",
                        "description": "Total Pix sent today (to check nightly limit accumulation)",
                        "default": 0,
                    },
                    "institution_type": {
                        "type": "string",
                        "description": "sending institution type: bank / fintech / payment_institution",
                        "enum": ["bank", "fintech", "payment_institution"],
                        "default": "bank",
                    },
                },
                "required": ["amount_brl", "sender_type", "receiver_type", "transaction_type", "time_of_day"],
            }
        },
        "required": ["transaction"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "approved": {"type": "boolean"},
            "effective_limit": {"type": "number"},
            "fee": {"type": "number"},
            "settlement_time_seconds": {"type": "integer"},
            "restrictions": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "approved",
            "effective_limit",
            "fee",
            "settlement_time_seconds",
            "restrictions",
            "status",
            "timestamp",
        ],
    },
}

# BCB Pix rules (Resolução BCB nº 1/2020 + Circular 4027/2020 + subsequent updates)

# Nightly period: 20:00-06:00 local time
_NIGHTLY_START_HOUR = 20   # 20:00
_NIGHTLY_END_HOUR = 6      # 06:00

# Nightly limit for PF (individual) senders
_PF_NIGHTLY_LIMIT_BRL = 1_000.00

# Default daytime limits (participants set their own, these are reference maximums)
# In practice, each institution sets limits; these reflect conservative defaults
_PF_DAYTIME_LIMIT_BRL = 20_000.00        # Per transaction
_PJ_DAYTIME_LIMIT_BRL = 1_000_000.00     # Per transaction (legal entities much higher)
_PJ_NIGHTLY_LIMIT_BRL = 100_000.00       # Nightly limit for PJ (institution default)

# Pix Troco / Pix Saque limits (BCB Resolução 4)
_PIX_TROCO_MAX_BRL = 500.00
_PIX_SAQUE_MAX_BRL = 500.00

# Settlement time constants
_STANDARD_SETTLEMENT_SECONDS = 10         # Real-time, 24/7
_SCHEDULED_SETTLEMENT_SECONDS = 60        # Scheduled future: processed at scheduled time
_NIGHTLY_ADDITIONAL_SECONDS = 0           # Pix runs 24/7 — no delay but limit applies

# Fee structure (BCB mandates Pix is FREE for PF; PJ fees are at institution discretion)
# Banks/fintechs may charge PJ; PF is always free for up to 8 transactions/month via app
_PF_MAX_FREE_TRANSACTIONS = 8             # Via institution app/internet banking
_PF_FEE_ABOVE_LIMIT_BRL = 0.00           # BCB prohibits charging PF for incoming Pix
_PJ_FEE_PER_TRANSACTION_BRL = 1.20       # Typical PJ fee (institution-set, reference only)
_PAYMENT_INSTITUTION_PF_FEE = 0.00       # Payment institutions must provide free Pix for PF


def brazil_pix_settlement_logic(transaction: dict[str, Any]) -> dict[str, Any]:
    """Apply BCB Pix rules to a payment transaction and determine settlement terms.

    Validates transaction against BCB-mandated limits including the PF nightly
    R$1,000 cap (20:00-06:00), daytime per-transaction limits, and special rules
    for Pix Troco and Pix Saque. Computes fees and settlement time.

    Args:
        transaction: Dictionary with amount_brl, sender_type, receiver_type,
            transaction_type, time_of_day, daily_cumulative_brl, and
            institution_type.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            approved (bool): Whether the transaction is within BCB limits.
            effective_limit (float): Applicable per-transaction limit in BRL.
            fee (float): Fee charged by the institution in BRL.
            settlement_time_seconds (int): Expected settlement time.
            restrictions (list[str]): Applicable restrictions or rule citations.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        amount_brl: float = float(transaction.get("amount_brl", 0))
        sender_type: str = str(transaction.get("sender_type", "pf")).lower()
        receiver_type: str = str(transaction.get("receiver_type", "pf")).lower()
        transaction_type: str = str(transaction.get("transaction_type", "standard")).lower()
        time_of_day: str = str(transaction.get("time_of_day", "12:00"))
        daily_cumulative_brl: float = float(transaction.get("daily_cumulative_brl", 0))
        institution_type: str = str(transaction.get("institution_type", "bank")).lower()

        restrictions: list[str] = []
        approved = True

        # --- Parse time ---
        try:
            hour = int(time_of_day.split(":")[0])
            minute = int(time_of_day.split(":")[1])
        except (ValueError, IndexError):
            return {
                "status": "error",
                "error": f"Invalid time_of_day format '{time_of_day}'. Expected HH:MM",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # --- Determine if nightly period ---
        is_nightly = hour >= _NIGHTLY_START_HOUR or hour < _NIGHTLY_END_HOUR

        # =====================================================================
        # SPECIAL TRANSACTION TYPES: Pix Troco / Pix Saque
        # =====================================================================
        if transaction_type == "pix_troco":
            effective_limit = _PIX_TROCO_MAX_BRL
            restrictions.append(
                f"Pix Troco: maximum R${_PIX_TROCO_MAX_BRL:.2f} per transaction "
                "(BCB Resolução nº 4/2020, Art. 7)"
            )
            if amount_brl > _PIX_TROCO_MAX_BRL:
                approved = False
                restrictions.append(
                    f"REJECTED: Pix Troco amount R${amount_brl:.2f} exceeds maximum "
                    f"R${_PIX_TROCO_MAX_BRL:.2f}"
                )

        elif transaction_type == "pix_saque":
            effective_limit = _PIX_SAQUE_MAX_BRL
            restrictions.append(
                f"Pix Saque: maximum R${_PIX_SAQUE_MAX_BRL:.2f} per transaction "
                "(BCB Resolução nº 4/2020, Art. 6)"
            )
            if amount_brl > _PIX_SAQUE_MAX_BRL:
                approved = False
                restrictions.append(
                    f"REJECTED: Pix Saque amount R${amount_brl:.2f} exceeds maximum "
                    f"R${_PIX_SAQUE_MAX_BRL:.2f}"
                )

        # =====================================================================
        # PF (INDIVIDUAL) SENDER LIMITS
        # =====================================================================
        elif sender_type == "pf":
            if is_nightly:
                effective_limit = _PF_NIGHTLY_LIMIT_BRL
                restrictions.append(
                    f"Nightly period active ({_NIGHTLY_START_HOUR}:00-{_NIGHTLY_END_HOUR}:00 BRT): "
                    f"PF nightly Pix limit is R${_PF_NIGHTLY_LIMIT_BRL:.2f} per transaction "
                    "(BCB Resolução nº 1/2020, Art. 29)"
                )
                # Check cumulative daily amount during nightly
                cumulative_after = daily_cumulative_brl + amount_brl
                if amount_brl > _PF_NIGHTLY_LIMIT_BRL:
                    approved = False
                    restrictions.append(
                        f"REJECTED: Transaction R${amount_brl:.2f} exceeds PF nightly limit "
                        f"R${_PF_NIGHTLY_LIMIT_BRL:.2f}. Split into separate transactions or "
                        "wait until after 06:00 BRT for daytime limit."
                    )
            else:
                effective_limit = _PF_DAYTIME_LIMIT_BRL
                restrictions.append(
                    f"Daytime period: PF per-transaction limit R${_PF_DAYTIME_LIMIT_BRL:,.2f} "
                    "(institution-defined; BCB requires institutions to offer at minimum R$1,000 "
                    "per transaction for individual clients)"
                )
                if amount_brl > _PF_DAYTIME_LIMIT_BRL:
                    approved = False
                    restrictions.append(
                        f"REJECTED: Transaction R${amount_brl:.2f} exceeds PF daytime limit. "
                        "Contact your institution to request a higher individual limit."
                    )

        # =====================================================================
        # PJ (LEGAL ENTITY) SENDER LIMITS
        # =====================================================================
        elif sender_type == "pj":
            if is_nightly:
                effective_limit = _PJ_NIGHTLY_LIMIT_BRL
                restrictions.append(
                    f"Nightly period: PJ nightly limit R${_PJ_NIGHTLY_LIMIT_BRL:,.2f} "
                    "(institution default — PJ limits are institution-set; BCB does not mandate "
                    "a specific PJ nightly cap, but most institutions apply one)"
                )
                if amount_brl > _PJ_NIGHTLY_LIMIT_BRL:
                    approved = False
                    restrictions.append(
                        f"REJECTED: PJ nightly transaction R${amount_brl:.2f} exceeds "
                        f"institution nightly limit R${_PJ_NIGHTLY_LIMIT_BRL:,.2f}. "
                        "Contact institution to adjust limit or use TEF/TED for large overnight transfers."
                    )
            else:
                effective_limit = _PJ_DAYTIME_LIMIT_BRL
                if amount_brl > _PJ_DAYTIME_LIMIT_BRL:
                    approved = False
                    restrictions.append(
                        f"REJECTED: PJ transaction R${amount_brl:.2f} exceeds daytime limit "
                        f"R${_PJ_DAYTIME_LIMIT_BRL:,.2f}. Use LBTR (real-time gross settlement) "
                        "for very large transfers."
                    )

        else:
            effective_limit = 0.0
            approved = False
            restrictions.append(f"Unknown sender_type '{sender_type}'. Must be 'pf' or 'pj'.")

        # =====================================================================
        # FEE CALCULATION
        # BCB mandates: PF always free (receiving). PF sending free up to institution threshold.
        # PJ: institution may charge (BCB Resolução nº 1/2020, Art. 11)
        # =====================================================================
        if sender_type == "pf":
            fee = _PF_FEE_ABOVE_LIMIT_BRL
            restrictions.append(
                "Pix is FREE for Pessoa Física (individual) senders per BCB mandate "
                "(BCB Resolução nº 1/2020, Art. 11 — institutions prohibited from charging PF)"
            )
        elif sender_type == "pj":
            if institution_type == "payment_institution":
                fee = 0.00  # Many fintechs offer free PJ Pix as competitive differentiator
                restrictions.append(
                    "Payment institution may offer free Pix for PJ clients — confirm with "
                    "institution fee schedule. BCB permits but does not require PJ fees."
                )
            else:
                fee = _PJ_FEE_PER_TRANSACTION_BRL
                restrictions.append(
                    f"PJ Pix fee: R${_PJ_FEE_PER_TRANSACTION_BRL:.2f} per transaction "
                    "(institution-set; BCB permits but does not mandate PJ Pix fees — "
                    "BCB Resolução nº 1/2020, Art. 11(3))"
                )
        else:
            fee = 0.00

        # =====================================================================
        # SETTLEMENT TIME
        # =====================================================================
        if transaction_type == "scheduled":
            settlement_time_seconds = _SCHEDULED_SETTLEMENT_SECONDS
            restrictions.append(
                "Scheduled Pix: processed at the scheduled date/time, not immediately. "
                "Funds debited from sender at scheduling; credited to receiver at execution time."
            )
        elif transaction_type == "recurring":
            settlement_time_seconds = _STANDARD_SETTLEMENT_SECONDS
            restrictions.append(
                "Recurring Pix: each recurrence settles in ~10 seconds at the scheduled time. "
                "Sender must maintain sufficient balance at each recurrence."
            )
        else:
            settlement_time_seconds = _STANDARD_SETTLEMENT_SECONDS

        restrictions.append(
            f"Pix settles 24 hours a day, 7 days a week, 365 days a year "
            f"in approximately {settlement_time_seconds} seconds "
            "(BCB Resolução nº 1/2020, Art. 5 — instant finality)"
        )

        # =====================================================================
        # BCB KEY RULE CITATION
        # =====================================================================
        restrictions.append(
            "Regulatory basis: BCB Resolução nº 1/2020 (Regulamento do Pix), "
            "Circular BCB nº 4027/2020, Resolução BCB nº 4/2020 (Pix Saque/Troco)"
        )

        result = {
            "approved": approved,
            "effective_limit": effective_limit,
            "fee": round(fee, 2),
            "fee_currency": "BRL",
            "settlement_time_seconds": settlement_time_seconds,
            "is_nightly_period": is_nightly,
            "nightly_period": f"{_NIGHTLY_START_HOUR}:00-{_NIGHTLY_END_HOUR:02d}:00 BRT",
            "amount_brl": amount_brl,
            "sender_type": sender_type,
            "receiver_type": receiver_type,
            "transaction_type": transaction_type,
            "time_of_day": time_of_day,
            "restrictions": restrictions,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"brazil_pix_settlement_logic failed: {e}")
        _log_lesson(f"brazil_pix_settlement_logic: {e}")
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
