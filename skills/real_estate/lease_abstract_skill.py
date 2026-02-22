"""
Executive Summary: Extracts key lease terms (dates, rent, escalations, options) from raw lease text using regex patterns.
Inputs: lease_text (str)
Outputs: dict with abstract_json (dict of extracted fields), extraction_confidence (float), missing_fields (list)
MCP Tool Name: lease_abstract_skill
"""
import os
import re
import logging
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "lease_abstract_skill",
    "description": (
        "Extracts key commercial lease terms from raw lease text using regex-based "
        "pattern matching. Targets commencement date, expiration date, base rent, "
        "escalation rate, renewal options, and break clauses. Returns confidence "
        "score and list of fields that could not be extracted."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "lease_text": {
                "type": "string",
                "description": "Full or partial lease document text to parse."
            }
        },
        "required": ["lease_text"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "abstract_json":          {"type": "object"},
                    "extraction_confidence":   {"type": "number"},
                    "missing_fields":         {"type": "array"}
                },
                "required": ["abstract_json", "extraction_confidence", "missing_fields"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Target fields and their extraction weight for confidence scoring
TARGET_FIELDS: list[str] = [
    "commencement_date",
    "expiration_date",
    "base_rent",
    "escalation_rate",
    "renewal_options",
    "break_clauses"
]

# Date patterns: covers common US CRE lease date formats
DATE_PATTERNS: list[str] = [
    r'\b(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})\b',                     # MM/DD/YYYY or MM-DD-YYYY
    r'\b(\w+ \d{1,2},?\s+\d{4})\b',                                 # Month DD, YYYY
    r'\b(\d{1,2}\s+\w+\s+\d{4})\b',                                 # DD Month YYYY
    r'\b((?:January|February|March|April|May|June|July|August|'
    r'September|October|November|December)\s+\d{1,2},?\s*\d{4})\b', # Full month name
]
COMBINED_DATE_RE = re.compile("|".join(DATE_PATTERNS), re.IGNORECASE)

# Commencement / lease start
COMMENCEMENT_RE = re.compile(
    r'(?:commencement\s+date|lease\s+commencement|term\s+commenc(?:es?|ing)|'
    r'start\s+date|beginning\s+of\s+term)[:\s,]+([^\n;.]{3,60})',
    re.IGNORECASE
)

# Expiration / termination
EXPIRATION_RE = re.compile(
    r'(?:expiration\s+date|lease\s+expir(?:es?|ation)|term\s+expir(?:es?|ation)|'
    r'termination\s+date|end\s+of\s+(?:the\s+)?(?:lease\s+)?term)[:\s,]+([^\n;.]{3,60})',
    re.IGNORECASE
)

# Base rent (annual or monthly)
BASE_RENT_RE = re.compile(
    r'(?:base\s+rent|minimum\s+rent|annual\s+base\s+rent|monthly\s+(?:base\s+)?rent)'
    r'[:\s,of]+\$?([\d,]+(?:\.\d{1,2})?)\s*(?:per\s+(?:month|annum|year|sf|square\s+foot))?',
    re.IGNORECASE
)

# Escalation / CPI / annual increase
ESCALATION_RE = re.compile(
    r'(?:annual\s+(?:rent\s+)?(?:increase|escalation|adjustment)|'
    r'(?:rent\s+)?escalat(?:es?|ion)|CPI\s+(?:adjustment|increase)|'
    r'(?:fixed\s+)?annual\s+(?:rent\s+)?bump)[:\s,]+(?:of\s+)?'
    r'([\d.]+\s*%|CPI\s*[+\-±]?\s*[\d.]*\s*%?|[\d.]+\s*(?:percent|per\s+cent))',
    re.IGNORECASE
)

# Renewal options
RENEWAL_RE = re.compile(
    r'(?:renewal\s+option[s]?|option\s+to\s+renew|extension\s+option[s]?)'
    r'[:\s,]+([^\n;.]{5,120})',
    re.IGNORECASE
)

# Break / termination clauses
BREAK_RE = re.compile(
    r'(?:break\s+clause|termination\s+option|early\s+termination(?:\s+right)?|'
    r'tenant[\'s]?\s+(?:right\s+to\s+)?terminat)[:\s,]+([^\n;.]{5,120})',
    re.IGNORECASE
)


def _extract_date_from_context(context: str) -> Optional[str]:
    """Pull the first date string found within a context snippet.

    Args:
        context: Raw text snippet adjacent to a labeled clause.

    Returns:
        First matched date string, or None if no date found.
    """
    match = COMBINED_DATE_RE.search(context)
    if match:
        return next((g for g in match.groups() if g is not None), None)
    return None


def lease_abstract_skill(
    lease_text: str,
    **kwargs: Any
) -> dict:
    """Extract key lease terms from raw lease document text.

    Uses a series of domain-specific regex patterns to locate and extract:
    commencement_date, expiration_date, base_rent, escalation_rate,
    renewal_options, and break_clauses.

    Confidence is computed as: extracted_fields / total_target_fields.
    A 10% penalty is applied per field where a label was found but no
    clean value could be parsed.

    Args:
        lease_text: Full or partial text of a commercial lease agreement.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (abstract_json, extraction_confidence,
        missing_fields, extracted_count, target_field_count), timestamp.

    Raises:
        ValueError: If lease_text is empty or not a string.
    """
    try:
        if not isinstance(lease_text, str):
            raise ValueError(f"lease_text must be a string, got {type(lease_text).__name__}.")
        if not lease_text.strip():
            raise ValueError("lease_text is empty.")

        abstract: dict = {}
        partial_matches: list[str] = []  # fields found but imperfectly parsed
        missing_fields: list[str] = []

        # --- commencement_date ---
        m = COMMENCEMENT_RE.search(lease_text)
        if m:
            date = _extract_date_from_context(m.group(1))
            if date:
                abstract["commencement_date"] = date.strip()
            else:
                abstract["commencement_date"] = m.group(1).strip()[:80]
                partial_matches.append("commencement_date")
        else:
            missing_fields.append("commencement_date")

        # --- expiration_date ---
        m = EXPIRATION_RE.search(lease_text)
        if m:
            date = _extract_date_from_context(m.group(1))
            if date:
                abstract["expiration_date"] = date.strip()
            else:
                abstract["expiration_date"] = m.group(1).strip()[:80]
                partial_matches.append("expiration_date")
        else:
            missing_fields.append("expiration_date")

        # --- base_rent ---
        m = BASE_RENT_RE.search(lease_text)
        if m:
            raw_rent = m.group(1).replace(",", "")
            try:
                abstract["base_rent"] = float(raw_rent)
            except ValueError:
                abstract["base_rent"] = m.group(1).strip()
                partial_matches.append("base_rent")
        else:
            missing_fields.append("base_rent")

        # --- escalation_rate ---
        m = ESCALATION_RE.search(lease_text)
        if m:
            raw_esc = m.group(1).strip()
            # Try to extract a numeric percentage
            pct_match = re.search(r'([\d.]+)\s*%', raw_esc)
            if pct_match:
                abstract["escalation_rate"] = f"{pct_match.group(1)}%"
            else:
                abstract["escalation_rate"] = raw_esc[:60]
                partial_matches.append("escalation_rate")
        else:
            missing_fields.append("escalation_rate")

        # --- renewal_options ---
        m = RENEWAL_RE.search(lease_text)
        if m:
            abstract["renewal_options"] = m.group(1).strip()[:200]
        else:
            missing_fields.append("renewal_options")

        # --- break_clauses ---
        m = BREAK_RE.search(lease_text)
        if m:
            abstract["break_clauses"] = m.group(1).strip()[:200]
        else:
            missing_fields.append("break_clauses")

        # Confidence: (extracted_fields / total) - 0.10 per partial
        extracted_count = len(TARGET_FIELDS) - len(missing_fields)
        raw_confidence = extracted_count / len(TARGET_FIELDS)
        partial_penalty = len(partial_matches) * 0.10
        extraction_confidence: float = round(max(0.0, raw_confidence - partial_penalty), 4)

        # Metadata
        abstract["_partial_fields"] = partial_matches
        abstract["_char_count_analyzed"] = len(lease_text)

        logger.info(
            "lease_abstract_skill: extracted=%d/%d, confidence=%.4f, missing=%s",
            extracted_count, len(TARGET_FIELDS), extraction_confidence, missing_fields
        )

        return {
            "status": "success",
            "data": {
                "abstract_json": abstract,
                "extraction_confidence": extraction_confidence,
                "missing_fields": missing_fields,
                "extracted_count": extracted_count,
                "target_field_count": len(TARGET_FIELDS),
                "partial_fields": partial_matches
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("lease_abstract_skill failed: %s", e)
        _log_lesson(f"lease_abstract_skill: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to the shared lessons log.

    Args:
        message: Description of the error or lesson to record.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError as log_err:
        logger.warning("Could not write to lessons.md: %s", log_err)
