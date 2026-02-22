"""
Executive Summary: GDPR-compliant PII removal and pseudonymisation for shared financial data — hashes or redacts PII fields while preserving non-PII financial data for analytics and reporting.
Inputs: data_records (list of dicts), pii_fields (list of str)
Outputs: scrubbed_records (list), fields_redacted (int), records_processed (int)
MCP Tool Name: gdpr_fin_data_scrub
"""
import os
import hashlib
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "gdpr_fin_data_scrub",
    "description": (
        "Removes or pseudonymises PII from financial data records per GDPR Article 5(1)(e) "
        "(storage limitation) and Article 25 (data protection by design). Uses SHA-256 hashing "
        "for reversible pseudonymisation or full redaction, preserving non-PII financial fields."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "data_records": {
                "type": "array",
                "description": "List of financial record dicts potentially containing PII",
                "items": {"type": "object"},
            },
            "pii_fields": {
                "type": "array",
                "description": "Field names to treat as PII (will be hashed or redacted)",
                "items": {"type": "string"},
                "default": [
                    "name",
                    "email",
                    "phone",
                    "ssn",
                    "address",
                    "date_of_birth",
                    "account_number",
                ],
            },
            "mode": {
                "type": "string",
                "description": "Processing mode: 'hash' (SHA-256 pseudonymisation) or 'redact' (replace with [REDACTED])",
                "enum": ["hash", "redact"],
                "default": "hash",
            },
            "salt": {
                "type": "string",
                "description": "Optional salt string for HMAC-style hashing (improves pseudonymisation security)",
            },
        },
        "required": ["data_records"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "scrubbed_records": {"type": "array", "items": {"type": "object"}},
            "fields_redacted": {"type": "integer"},
            "records_processed": {"type": "integer"},
            "pii_fields_found": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "scrubbed_records",
            "fields_redacted",
            "records_processed",
            "status",
            "timestamp",
        ],
    },
}

_DEFAULT_PII_FIELDS: list[str] = [
    "name",
    "first_name",
    "last_name",
    "full_name",
    "email",
    "email_address",
    "phone",
    "phone_number",
    "mobile",
    "ssn",
    "social_security_number",
    "national_id",
    "passport_number",
    "address",
    "street_address",
    "postal_code",
    "date_of_birth",
    "dob",
    "birthdate",
    "account_number",
    "iban",
    "routing_number",
    "tax_id",
    "ip_address",
    "device_id",
]


def gdpr_fin_data_scrub(
    data_records: list[dict[str, Any]],
    pii_fields: list[str] | None = None,
    mode: str = "hash",
    salt: str = "",
) -> dict[str, Any]:
    """Scrub PII from financial data records using hashing or redaction.

    Processes each record in the input list, replacing identified PII fields
    with a SHA-256 hash (pseudonymisation) or a redaction placeholder. All
    non-PII financial data is preserved intact for analytics use.

    Args:
        data_records: List of financial record dictionaries.
        pii_fields: List of field names to treat as PII. Defaults to a
            comprehensive set of 20 common PII fields if not provided.
        mode: Processing mode — "hash" for SHA-256 pseudonymisation or
            "redact" for full replacement with "[REDACTED]".
        salt: Optional salt string prepended before hashing for added
            security against rainbow table attacks.

    Returns:
        Dictionary with keys:
            status (str): "success" or "error".
            scrubbed_records (list[dict]): Processed records with PII removed.
            fields_redacted (int): Total number of individual PII field values
                processed across all records.
            records_processed (int): Total number of records processed.
            pii_fields_found (list[str]): Unique PII field names that were
                actually present in the data.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        if pii_fields is None or len(pii_fields) == 0:
            pii_fields = _DEFAULT_PII_FIELDS

        # Normalise field names for case-insensitive matching
        pii_field_set: set[str] = {f.lower().strip() for f in pii_fields}

        scrubbed_records: list[dict[str, Any]] = []
        fields_redacted_count: int = 0
        pii_fields_found: set[str] = set()

        for record in data_records:
            if not isinstance(record, dict):
                scrubbed_records.append(record)
                continue

            scrubbed = {}
            for key, value in record.items():
                key_lower = key.lower().strip()
                if key_lower in pii_field_set:
                    pii_fields_found.add(key)
                    fields_redacted_count += 1
                    if mode == "hash" and value is not None:
                        raw = f"{salt}{str(value)}"
                        scrubbed[key] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
                    else:
                        scrubbed[key] = "[REDACTED]"
                    # Add a processing metadata field for auditability
                    scrubbed[f"_gdpr_{key}_processed"] = mode
                else:
                    scrubbed[key] = value

            scrubbed["_gdpr_scrubbed"] = True
            scrubbed["_gdpr_mode"] = mode
            scrubbed["_gdpr_processed_at"] = datetime.now(timezone.utc).isoformat()
            scrubbed_records.append(scrubbed)

        # Build GDPR Article 30 record of processing note
        processing_record = {
            "article_30_note": "Data scrubbing performed under GDPR Art. 25 (data protection by design) "
            "and Art. 5(1)(e) (storage limitation)",
            "lawful_basis": "Pseudonymisation / anonymisation — GDPR Art. 4(5)",
            "data_subjects_affected": len(data_records),
            "fields_pseudonymised_or_redacted": fields_redacted_count,
            "pseudonymisation_method": (
                "SHA-256 with optional salt" if mode == "hash" else "Full redaction"
            ),
        }

        result = {
            "scrubbed_records": scrubbed_records,
            "fields_redacted": fields_redacted_count,
            "records_processed": len(data_records),
            "pii_fields_found": sorted(pii_fields_found),
            "pii_fields_checked": sorted(pii_field_set),
            "mode": mode,
            "processing_record": processing_record,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"gdpr_fin_data_scrub failed: {e}")
        _log_lesson(f"gdpr_fin_data_scrub: {e}")
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
