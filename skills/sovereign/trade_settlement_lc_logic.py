"""
Executive Summary: Validates digital Letters of Credit against UCP 600 rules, checks document completeness, and provides settlement recommendations.
Inputs: lc_data (dict: applicant, beneficiary, amount, currency, goods_description, shipping_date, expiry_date, documents_required)
Outputs: valid (bool), missing_documents (list), days_to_expiry (int), ucp600_compliance (dict), settlement_recommendation (str)
MCP Tool Name: trade_settlement_lc_logic
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone, date

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "trade_settlement_lc_logic",
    "description": "Validates Letters of Credit against UCP 600 international rules, checks document completeness, and generates settlement recommendations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "lc_data": {
                "type": "object",
                "description": "Letter of Credit terms",
                "properties": {
                    "applicant": {"type": "string", "description": "LC applicant (buyer/importer)"},
                    "beneficiary": {"type": "string", "description": "LC beneficiary (seller/exporter)"},
                    "amount": {"type": "number", "description": "LC amount in specified currency"},
                    "currency": {"type": "string", "description": "ISO 4217 currency code"},
                    "goods_description": {"type": "string", "description": "Description of goods"},
                    "shipping_date": {"type": "string", "description": "Latest shipment date ISO YYYY-MM-DD"},
                    "expiry_date": {"type": "string", "description": "LC expiry date ISO YYYY-MM-DD"},
                    "documents_required": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of required document names"
                    },
                    "documents_presented": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of documents actually presented (optional for validation)"
                    },
                    "lc_type": {"type": "string", "description": "irrevocable or revocable (default: irrevocable)"},
                    "confirmation": {"type": "string", "description": "confirmed or unconfirmed (default: unconfirmed)"}
                },
                "required": ["applicant", "beneficiary", "amount", "currency", "goods_description", "shipping_date", "expiry_date", "documents_required"]
            }
        },
        "required": ["lc_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "valid": {"type": "boolean"},
                    "missing_documents": {"type": "array"},
                    "days_to_expiry": {"type": "integer"},
                    "ucp600_compliance": {"type": "object"},
                    "settlement_recommendation": {"type": "string"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# UCP 600 standard document set — Article 18-28 references
UCP600_STANDARD_DOCUMENTS = {
    "commercial invoice",
    "bill of lading",
    "packing list",
    "certificate of origin",
    "insurance certificate",
}

# Minimum document list that UCP 600 transactions should include
UCP600_MINIMUM_REQUIRED = {
    "commercial invoice",
    "bill of lading",
}

# Supported ISO 4217 codes for basic validation
VALID_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "CHF", "CNY", "CNH", "AED", "SAR",
    "SGD", "HKD", "AUD", "CAD", "NOK", "SEK", "INR", "BRL", "ZAR",
    "KRW", "MXN", "TRY", "RUB", "NGN", "KES", "GHS",
}

# UCP 600 presentation period: default 21 days after shipment (Article 14c)
UCP600_PRESENTATION_DAYS = 21


def _parse_date(date_str: str) -> date:
    """Parse a date string in YYYY-MM-DD format.

    Args:
        date_str: ISO-format date string.

    Returns:
        date: Python date object.

    Raises:
        ValueError: If the string cannot be parsed as YYYY-MM-DD.
    """
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format '{date_str}'; expected YYYY-MM-DD")


def trade_settlement_lc_logic(
    lc_data: dict[str, Any],
    **kwargs: Any
) -> dict[str, Any]:
    """Validate a Letter of Credit against UCP 600 rules and recommend settlement action.

    Performs structural validation of the LC fields, checks document
    requirements against UCP 600 Article 14 (Standard for Examination of
    Documents), verifies dates, and produces a settlement recommendation.

    UCP 600 key rules checked:
      - Article 6: LC must be irrevocable by default
      - Article 14c: Documents must be presented within 21 days of shipment
      - Article 14d: Documents must not conflict with each other or the LC
      - Article 18: Commercial invoice must match LC amount/currency
      - Article 20: Bill of lading required for sea/multimodal transport
      - Expiry date must be after shipping date

    Args:
        lc_data: Dictionary of LC terms. Required keys: 'applicant', 'beneficiary',
            'amount', 'currency', 'goods_description', 'shipping_date',
            'expiry_date', 'documents_required'. Optional: 'documents_presented',
            'lc_type', 'confirmation'.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Validation results including valid (bool),
              missing_documents (list), days_to_expiry (int),
              ucp600_compliance (dict of named rule checks),
              settlement_recommendation (str), and lc_summary.
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        applicant = str(lc_data.get("applicant", "")).strip()
        beneficiary = str(lc_data.get("beneficiary", "")).strip()
        amount = float(lc_data.get("amount", 0.0))
        currency = str(lc_data.get("currency", "")).upper().strip()
        goods_description = str(lc_data.get("goods_description", "")).strip()
        shipping_date_str = str(lc_data.get("shipping_date", "")).strip()
        expiry_date_str = str(lc_data.get("expiry_date", "")).strip()
        documents_required: list[str] = [d.lower().strip() for d in lc_data.get("documents_required", [])]
        documents_presented: list[str] = [d.lower().strip() for d in lc_data.get("documents_presented", [])]
        lc_type = str(lc_data.get("lc_type", "irrevocable")).lower().strip()
        confirmation = str(lc_data.get("confirmation", "unconfirmed")).lower().strip()

        today = datetime.now(timezone.utc).date()

        # Parse dates
        shipping_date = _parse_date(shipping_date_str)
        expiry_date = _parse_date(expiry_date_str)

        days_to_expiry: int = (expiry_date - today).days
        days_shipping_to_expiry: int = (expiry_date - shipping_date).days

        # --- UCP 600 compliance checks ---
        ucp600_compliance: dict[str, dict[str, Any]] = {}

        # Art 6: LC type (all modern LCs should be irrevocable)
        ucp600_compliance["art6_irrevocable"] = {
            "rule": "Article 6 — LC must be irrevocable",
            "passed": lc_type == "irrevocable",
            "detail": f"LC type is '{lc_type}'" + (
                "" if lc_type == "irrevocable" else "; REVOCABLE LCs are obsolete under UCP 600"
            ),
        }

        # Art 14c: Presentation period (expiry must allow at least 21 days after shipment)
        art14c_passed = days_shipping_to_expiry >= UCP600_PRESENTATION_DAYS
        ucp600_compliance["art14c_presentation_period"] = {
            "rule": f"Article 14c — Min {UCP600_PRESENTATION_DAYS} days between shipment and expiry",
            "passed": art14c_passed,
            "shipping_date": shipping_date_str,
            "expiry_date": expiry_date_str,
            "days_between": days_shipping_to_expiry,
            "detail": (
                f"{days_shipping_to_expiry} days between shipment and expiry"
                if art14c_passed
                else f"Only {days_shipping_to_expiry} days — UCP 600 requires minimum {UCP600_PRESENTATION_DAYS}"
            ),
        }

        # Expiry date check: must be in the future
        not_expired = days_to_expiry >= 0
        ucp600_compliance["expiry_not_lapsed"] = {
            "rule": "LC expiry date must not have passed",
            "passed": not_expired,
            "days_to_expiry": days_to_expiry,
            "detail": (
                f"{days_to_expiry} days remaining" if not_expired
                else f"LC EXPIRED {abs(days_to_expiry)} days ago"
            ),
        }

        # Shipping date must precede expiry
        shipping_before_expiry = shipping_date < expiry_date
        ucp600_compliance["shipping_before_expiry"] = {
            "rule": "Shipping date must precede LC expiry date",
            "passed": shipping_before_expiry,
            "detail": (
                "Shipping date precedes expiry"
                if shipping_before_expiry
                else "ERROR: Shipping date is after expiry date"
            ),
        }

        # Art 18: Commercial invoice
        has_invoice = "commercial invoice" in documents_required
        ucp600_compliance["art18_commercial_invoice"] = {
            "rule": "Article 18 — Commercial invoice required",
            "passed": has_invoice,
            "detail": "Commercial invoice present in required documents" if has_invoice else "Missing: commercial invoice",
        }

        # Art 20: Bill of lading (for sea transport)
        has_bol = "bill of lading" in documents_required
        ucp600_compliance["art20_bill_of_lading"] = {
            "rule": "Article 20 — Bill of lading required for sea/multimodal shipment",
            "passed": has_bol,
            "detail": "Bill of lading present" if has_bol else "Missing: bill of lading (required for sea transport)",
        }

        # Amount validity
        amount_valid = amount > 0
        ucp600_compliance["amount_positive"] = {
            "rule": "LC amount must be positive",
            "passed": amount_valid,
            "amount": amount,
            "currency": currency,
            "detail": f"Amount: {amount:,.2f} {currency}" if amount_valid else "Amount must be > 0",
        }

        # Currency validity
        currency_valid = currency in VALID_CURRENCIES
        ucp600_compliance["currency_recognized"] = {
            "rule": "Currency must be recognized ISO 4217 code",
            "passed": currency_valid,
            "currency": currency,
            "detail": f"Currency '{currency}' recognized" if currency_valid else f"Currency '{currency}' not in recognized list",
        }

        # Parties distinct
        parties_distinct = applicant.lower() != beneficiary.lower() and bool(applicant) and bool(beneficiary)
        ucp600_compliance["parties_distinct"] = {
            "rule": "Applicant and beneficiary must be distinct named parties",
            "passed": parties_distinct,
            "detail": "Parties are distinct" if parties_distinct else "Applicant and beneficiary are the same or blank",
        }

        # Goods description not overly vague
        goods_adequate = len(goods_description) >= 10
        ucp600_compliance["goods_description_adequate"] = {
            "rule": "Goods description must be adequately specific (min 10 chars)",
            "passed": goods_adequate,
            "detail": f"Goods: '{goods_description[:80]}'" if goods_adequate else "Goods description too vague",
        }

        # --- Missing documents (if presented set is provided) ---
        missing_documents: list[str] = []
        presented_set = set(documents_presented)
        required_set = set(documents_required)

        if documents_presented:
            missing_documents = sorted(required_set - presented_set)

        # --- Overall validity ---
        compliance_results = [v["passed"] for v in ucp600_compliance.values()]
        all_passed = all(compliance_results)
        critical_fields = [
            ucp600_compliance["art6_irrevocable"]["passed"],
            ucp600_compliance["art14c_presentation_period"]["passed"],
            ucp600_compliance["expiry_not_lapsed"]["passed"],
            ucp600_compliance["shipping_before_expiry"]["passed"],
            ucp600_compliance["art18_commercial_invoice"]["passed"],
            ucp600_compliance["amount_positive"]["passed"],
            ucp600_compliance["parties_distinct"]["passed"],
        ]
        critical_pass = all(critical_fields)
        failed_checks = [k for k, v in ucp600_compliance.items() if not v["passed"]]

        valid: bool = critical_pass and not missing_documents

        # --- Settlement recommendation ---
        if not not_expired:
            settlement_recommendation = "REJECT — LC has expired. Applicant must issue a new LC or amendment."
        elif not critical_pass:
            settlement_recommendation = (
                f"REJECT — {len(failed_checks)} critical UCP 600 compliance failure(s): "
                f"{', '.join(failed_checks[:3])}. Resolve before presentation."
            )
        elif missing_documents:
            settlement_recommendation = (
                f"ON HOLD — {len(missing_documents)} required document(s) not presented: "
                f"{', '.join(missing_documents[:3])}. Present all documents within {days_to_expiry} days."
            )
        elif days_to_expiry <= 5:
            settlement_recommendation = (
                f"URGENT SETTLEMENT — LC expires in {days_to_expiry} days. "
                "Complete document presentation and bank examination immediately."
            )
        elif days_to_expiry <= 21:
            settlement_recommendation = (
                f"SETTLE PROMPTLY — {days_to_expiry} days to expiry. "
                "Initiate bank examination and SWIFT MT700 settlement."
            )
        else:
            settlement_recommendation = (
                f"APPROVE FOR SETTLEMENT — All UCP 600 checks passed. "
                f"{days_to_expiry} days remaining. Process SWIFT MT700 payment."
            )

        result: dict[str, Any] = {
            "valid": valid,
            "missing_documents": missing_documents,
            "days_to_expiry": days_to_expiry,
            "days_shipping_to_expiry": days_shipping_to_expiry,
            "ucp600_compliance": ucp600_compliance,
            "settlement_recommendation": settlement_recommendation,
            "failed_compliance_checks": failed_checks,
            "passed_checks": len(compliance_results) - len(failed_checks),
            "total_checks": len(compliance_results),
            "lc_summary": {
                "applicant": applicant,
                "beneficiary": beneficiary,
                "amount": amount,
                "currency": currency,
                "lc_type": lc_type,
                "confirmation": confirmation,
                "shipping_date": shipping_date_str,
                "expiry_date": expiry_date_str,
                "goods_description": goods_description[:200],
                "documents_required": documents_required,
                "documents_presented": documents_presented,
            },
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"trade_settlement_lc_logic failed: {e}")
        _log_lesson(f"trade_settlement_lc_logic: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson/error entry to the shared lessons log.

    Args:
        message: Human-readable error or lesson description to append.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception as log_err:
        logger.warning(f"_log_lesson write failed: {log_err}")
