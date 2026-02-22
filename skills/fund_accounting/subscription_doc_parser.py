"""
Executive Summary: Parses LP subscription agreement text using regex to extract LP name, committed capital, entity type, and jurisdiction with confidence scoring.

Inputs: document_text (str — extracted PDF text)
Outputs: dict with lp_name (str), committed_amount (float), entity_type (str), jurisdiction (str), confidence_scores (dict)
MCP Tool Name: subscription_doc_parser
"""
import os
import re
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "subscription_doc_parser",
    "description": (
        "Parses LP subscription agreement text extracted from PDF to identify "
        "the limited partner name, committed capital amount, legal entity type, "
        "and jurisdiction. Returns structured data with per-field confidence scores."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "document_text": {
                "type": "string",
                "description": "Raw text extracted from the subscription agreement PDF"
            }
        },
        "required": ["document_text"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "lp_name": {"type": "string"},
            "committed_amount": {"type": "number"},
            "entity_type": {"type": "string"},
            "jurisdiction": {"type": "string"},
            "confidence_scores": {
                "type": "object",
                "properties": {
                    "lp_name": {"type": "number"},
                    "committed_amount": {"type": "number"},
                    "entity_type": {"type": "number"},
                    "jurisdiction": {"type": "number"},
                    "overall": {"type": "number"}
                }
            },
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["lp_name", "committed_amount", "entity_type", "jurisdiction", "confidence_scores", "status", "timestamp"]
    }
}

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# LP Name: looks for "Subscriber:", "Investor Name:", "Limited Partner:", etc.
_LP_NAME_PATTERNS: list[tuple[re.Pattern, float]] = [
    (re.compile(r"(?:Subscriber|Investor Name|Limited Partner|Subscriber Name|Name of Subscriber)[:\s]+([A-Z][A-Za-z0-9\s,.'&()-]{2,80})", re.IGNORECASE), 0.95),
    (re.compile(r"^([A-Z][A-Za-z0-9\s,.'&()-]{4,60})\s+(?:LLC|LP|L\.P\.|L\.L\.C\.|Trust|Fund|Partners|Capital)", re.MULTILINE), 0.70),
    (re.compile(r"(?:by and between the Fund and\s+)([A-Z][A-Za-z0-9\s,.'&()-]{4,60})", re.IGNORECASE), 0.80),
]

# Committed Amount: dollar figures near commitment-related words
_AMOUNT_PATTERNS: list[tuple[re.Pattern, float]] = [
    (re.compile(r"(?:Capital Commitment|Commitment Amount|Total Commitment|Subscribed Amount|Subscription Amount)[:\s]*\$?\s*([\d,]+(?:\.\d{1,2})?)\s*(?:USD|dollars?)?", re.IGNORECASE), 0.95),
    (re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)\s*(?:million|MM|M)\b", re.IGNORECASE), 0.80),
    (re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)\b", re.IGNORECASE), 0.50),
]

# Entity Type
_ENTITY_PATTERNS: list[tuple[re.Pattern, str, float]] = [
    (re.compile(r"\bL\.?L\.?C\.?\b", re.IGNORECASE), "LLC", 0.90),
    (re.compile(r"\bL\.?L\.?P\.?\b", re.IGNORECASE), "LLP", 0.90),
    (re.compile(r"\b(?:Limited Partnership|L\.?P\.?)\b", re.IGNORECASE), "LP", 0.90),
    (re.compile(r"\b(?:Revocable|Irrevocable|Living|Family)?\s*Trust\b", re.IGNORECASE), "Trust", 0.85),
    (re.compile(r"\bCorporation\b|\bCorp\.?\b|\bInc\.?\b", re.IGNORECASE), "Corporation", 0.85),
    (re.compile(r"\bFamily\s+Office\b", re.IGNORECASE), "Family Office", 0.85),
    (re.compile(r"\bEndowment\b", re.IGNORECASE), "Endowment", 0.80),
    (re.compile(r"\bFoundation\b", re.IGNORECASE), "Foundation", 0.80),
    (re.compile(r"\bPension\s+Fund\b|\bRetirement\s+Fund\b", re.IGNORECASE), "Pension Fund", 0.85),
    (re.compile(r"\bIndividual\b|\bNatural\s+Person\b", re.IGNORECASE), "Individual", 0.75),
]

# US States
_US_STATES = {
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming", "District of Columbia",
}

_STATE_ABBREVS = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC",
}

_COUNTRY_PATTERN = re.compile(
    r"\b(United Kingdom|UK|Cayman Islands|British Virgin Islands|BVI|"
    r"Luxembourg|Ireland|Singapore|Switzerland|Canada|Australia|"
    r"Germany|France|Japan|Netherlands|Hong Kong|UAE|United Arab Emirates)\b",
    re.IGNORECASE
)

_JURISDICTION_PATTERNS: list[tuple[re.Pattern, float]] = [
    (re.compile(r"(?:organized|formed|incorporated|registered|domiciled)\s+(?:under the laws of|in)\s+(?:the\s+)?(?:State of\s+)?([A-Za-z\s]+?)(?:\s*[,.]|\s+and\b)", re.IGNORECASE), 0.90),
    (re.compile(r"(?:State of\s+)(" + "|".join(re.escape(s) for s in _US_STATES) + r")\b", re.IGNORECASE), 0.85),
]


def _parse_amount(raw: str) -> float:
    """Convert a raw currency string to a float, handling commas and million suffixes.

    Args:
        raw: Raw matched string, e.g. '5,000,000' or '5.5' (where context is millions).

    Returns:
        Float dollar amount.
    """
    cleaned = raw.replace(",", "").strip()
    return float(cleaned)


def _extract_lp_name(text: str) -> tuple[str, float]:
    """Attempt to extract LP name from document text.

    Args:
        text: Full subscription document text.

    Returns:
        Tuple of (lp_name, confidence_score).
    """
    for pattern, confidence in _LP_NAME_PATTERNS:
        match = pattern.search(text)
        if match:
            name = match.group(1).strip().rstrip(".,;")
            if len(name) >= 3:
                return name, confidence
    return "UNKNOWN", 0.0


def _extract_amount(text: str) -> tuple[float, float]:
    """Attempt to extract committed capital amount from document text.

    Args:
        text: Full subscription document text.

    Returns:
        Tuple of (amount_float, confidence_score).
    """
    for pattern, confidence in _AMOUNT_PATTERNS:
        match = pattern.search(text)
        if match:
            raw = match.group(1)
            amount = _parse_amount(raw)
            # Handle "million" multiplier in text near the match
            full_match_text = match.group(0)
            if re.search(r"\b(?:million|MM|M)\b", full_match_text, re.IGNORECASE):
                amount *= 1_000_000
            if amount > 0:
                return amount, confidence
    return 0.0, 0.0


def _extract_entity_type(text: str) -> tuple[str, float]:
    """Detect legal entity type from document text.

    Args:
        text: Full subscription document text.

    Returns:
        Tuple of (entity_type, confidence_score).
    """
    # Use first 2000 chars for context-weighted matching
    header_text = text[:2000]
    for pattern, entity_name, confidence in _ENTITY_PATTERNS:
        if pattern.search(header_text):
            return entity_name, confidence
    for pattern, entity_name, confidence in _ENTITY_PATTERNS:
        if pattern.search(text):
            return entity_name, confidence * 0.85
    return "UNKNOWN", 0.0


def _extract_jurisdiction(text: str) -> tuple[str, float]:
    """Extract jurisdiction (state or country) from document text.

    Args:
        text: Full subscription document text.

    Returns:
        Tuple of (jurisdiction, confidence_score).
    """
    for pattern, confidence in _JURISDICTION_PATTERNS:
        match = pattern.search(text)
        if match:
            jur = match.group(1).strip().title()
            if jur:
                return jur, confidence

    # Try state abbreviation lookup (e.g. "Delaware LLC")
    state_match = re.search(
        r"\b(" + "|".join(re.escape(s) for s in _US_STATES) + r")\b",
        text, re.IGNORECASE
    )
    if state_match:
        return state_match.group(1).title(), 0.65

    # Try country
    country_match = _COUNTRY_PATTERN.search(text)
    if country_match:
        return country_match.group(1).title(), 0.70

    return "UNKNOWN", 0.0


def subscription_doc_parser(**kwargs: Any) -> dict:
    """Parse LP subscription agreement text to extract structured investor data.

    Uses layered regex patterns with priority ordering. Each field reports
    an independent confidence score (0.0–1.0) based on which pattern matched.
    Overall confidence is the unweighted mean of all field scores.

    Args:
        **kwargs: Keyword arguments containing:
            document_text (str): Raw text extracted from the subscription PDF.

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict): Parsed fields and confidence scores:
                - lp_name (str): Limited partner legal name
                - committed_amount (float): Dollar commitment
                - entity_type (str): LLC, LP, Trust, etc.
                - jurisdiction (str): State or country of formation
                - confidence_scores (dict): Per-field and overall confidence
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        document_text: str = kwargs.get("document_text", "")

        if not document_text or not document_text.strip():
            raise ValueError("document_text is empty — cannot parse subscription document")

        lp_name, lp_conf = _extract_lp_name(document_text)
        committed_amount, amount_conf = _extract_amount(document_text)
        entity_type, entity_conf = _extract_entity_type(document_text)
        jurisdiction, jur_conf = _extract_jurisdiction(document_text)

        scores = {
            "lp_name": lp_conf,
            "committed_amount": amount_conf,
            "entity_type": entity_conf,
            "jurisdiction": jur_conf,
        }
        scores["overall"] = round(sum(scores.values()) / len(scores), 4)

        result = {
            "lp_name": lp_name,
            "committed_amount": committed_amount,
            "entity_type": entity_type,
            "jurisdiction": jurisdiction,
            "confidence_scores": scores,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"subscription_doc_parser failed: {e}")
        _log_lesson(f"subscription_doc_parser: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the shared lessons log.

    Args:
        message: The lesson or error description to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
