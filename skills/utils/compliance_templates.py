"""Shared filing/template builders for compliance skills."""
from __future__ import annotations

from typing import Any, Iterable

from .time import get_iso_timestamp


def build_boir_payload(
    reporting_company: dict[str, Any],
    beneficial_owners: list[dict[str, Any]],
    *,
    company_applicants: list[dict[str, Any]] | None = None,
    submission_type: str = "initial",
    exemptions: dict[str, Any] | None = None,
    attachments: list[str] | None = None,
) -> dict[str, Any]:
    """Return a FinCEN BOIR JSON payload with standard metadata."""

    payload = {
        "form": "FinCEN_BOIR",
        "version": "2024-01",
        "submission_type": submission_type,
        "reporting_company": reporting_company,
        "beneficial_owners": beneficial_owners,
        "company_applicants": company_applicants or [],
        "exemptions": exemptions or {},
        "attachments": attachments or [],
        "metadata": {
            "generated_at": get_iso_timestamp(),
            "schema": "FinCEN-BOIR-v1",
        },
    }
    return payload


def build_form_pf_payload(
    section_one: dict[str, Any],
    section_two: dict[str, Any] | None,
    *,
    large_adviser: bool,
    filing_frequency: str,
    adviser_metadata: dict[str, Any],
) -> dict[str, Any]:
    """Return a structured Form PF payload ready for PFRD upload."""

    return {
        "form": "SEC_FORM_PF",
        "version": "2024-05",
        "large_adviser": large_adviser,
        "filing_frequency": filing_frequency,
        "sections": {
            "section_1": section_one,
            "section_2": section_two,
        },
        "metadata": {
            "generated_at": get_iso_timestamp(),
            "adviser": adviser_metadata,
        },
    }


def build_schedule_d_payload(
    line_items: list[dict[str, Any]],
    totals: dict[str, Any],
    *,
    tax_year: str,
) -> dict[str, Any]:
    """Return IRS Schedule D / Form 8949 payload with audit metadata."""

    return {
        "form": "IRS_SCHEDULE_D",
        "version": "2024-01",
        "tax_year": tax_year,
        "line_items": line_items,
        "totals": totals,
        "metadata": {
            "generated_at": get_iso_timestamp(),
            "source": "Snowdrop",
        },
    }


def build_sfdr_disclosure(
    classification: str,
    disclosure_requirements: list[str],
    *,
    taxonomy_alignment_pct: float,
    pai_required: bool,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Return SFDR Annex style disclosure summary."""

    return {
        "framework": "EU_SFDR",
        "article": classification,
        "taxonomy_alignment_pct": round(taxonomy_alignment_pct, 2),
        "pai_statement_required": pai_required,
        "disclosure_requirements": disclosure_requirements,
        "warnings": warnings or [],
        "metadata": {"generated_at": get_iso_timestamp()},
    }


def build_gst_summary(
    breakdown: dict[str, float],
    *,
    exemptions: Iterable[str],
    filings: Iterable[str],
) -> dict[str, Any]:
    """Return GST return helper payload for GSTR-1/3B workflows."""

    return {
        "form": "INDIA_GST",
        "version": "2024-01",
        "tax_breakdown": breakdown,
        "exemptions_applied": list(exemptions),
        "filings": list(filings),
        "metadata": {"generated_at": get_iso_timestamp()},
    }


def build_gdpr_processing_log(
    scrubbed_records: list[dict[str, Any]],
    *,
    fields_redacted: int,
    records_processed: int,
    pii_fields_found: list[str],
    mode: str,
) -> dict[str, Any]:
    """Return GDPR Article 30 processing bundle."""

    return {
        "framework": "GDPR",
        "mode": mode,
        "records_processed": records_processed,
        "fields_redacted": fields_redacted,
        "pii_fields_found": pii_fields_found,
        "scrubbed_records": scrubbed_records,
        "metadata": {
            "generated_at": get_iso_timestamp(),
            "article_30_reference": "Processing log maintained per GDPR Art. 30 and Art. 32",
        },
    }
