"""
Executive Summary: Transforms legacy Argus-style raw CRE data dicts into a standardized JSON schema with warnings.
Inputs: argus_data (dict: property_name, noi, cap_rate, occupancy, lease_expiry_schedule)
Outputs: dict with standardized_json (dict), fields_mapped (int), warnings (list)
MCP Tool Name: argus_to_json_transformer
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "argus_to_json_transformer",
    "description": (
        "Transforms legacy Argus-style raw commercial real estate data dictionaries "
        "into a clean, standardized JSON schema with consistent field naming, "
        "type coercion, and a warnings list for missing or suspicious values."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "argus_data": {
                "type": "object",
                "description": (
                    "Raw Argus export dict. Expected raw fields: property_name (str), "
                    "noi (number), cap_rate (number), occupancy (number), "
                    "lease_expiry_schedule (list of dicts or raw string)."
                )
            }
        },
        "required": ["argus_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "standardized_json": {"type": "object"},
                    "fields_mapped": {"type": "integer"},
                    "warnings": {"type": "array"}
                },
                "required": ["standardized_json", "fields_mapped", "warnings"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Canonical field mappings: (argus raw variants) -> standard name
FIELD_ALIASES: dict[str, list[str]] = {
    "property_name":        ["property_name", "prop_name", "asset_name", "name", "Property Name"],
    "noi":                  ["noi", "net_operating_income", "NOI", "Net Operating Income"],
    "cap_rate":             ["cap_rate", "cap rate", "capitalization_rate", "Cap Rate", "CapRate"],
    "occupancy":            ["occupancy", "occupancy_rate", "occ_rate", "Occupancy", "Occupancy Rate"],
    "lease_expiry_schedule":["lease_expiry_schedule", "lease_schedule", "leases", "Lease Schedule",
                             "Lease Expiry", "lease_expirations"]
}


def argus_to_json_transformer(
    argus_data: dict,
    **kwargs: Any
) -> dict:
    """Transform a raw Argus export dict into the Snowdrop CRE standard schema.

    Applies alias resolution, type coercion, occupancy normalization (percent to decimal),
    cap_rate normalization, and lease schedule parsing. Generates warnings for missing
    required fields, out-of-range values, and unrecognized fields.

    Args:
        argus_data: Raw Argus-style export dictionary with arbitrary field names.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (standardized_json, fields_mapped, warnings),
        timestamp.

    Raises:
        ValueError: If argus_data is not a dict.
    """
    try:
        if not isinstance(argus_data, dict):
            raise ValueError(f"argus_data must be a dict, got {type(argus_data).__name__}.")

        warnings: list[str] = []
        standardized: dict = {}
        fields_mapped: int = 0
        unrecognized_fields: list[str] = set(argus_data.keys())

        def _resolve(canonical: str) -> Any:
            """Find the first matching alias in argus_data."""
            for alias in FIELD_ALIASES[canonical]:
                if alias in argus_data:
                    unrecognized_fields.discard(alias)
                    return argus_data[alias]
            return None

        # --- property_name ---
        raw_name = _resolve("property_name")
        if raw_name is None:
            warnings.append("Missing field: property_name. Defaulting to 'UNKNOWN'.")
            standardized["property_name"] = "UNKNOWN"
        else:
            standardized["property_name"] = str(raw_name).strip()
            fields_mapped += 1

        # --- noi ---
        raw_noi = _resolve("noi")
        if raw_noi is None:
            warnings.append("Missing field: noi.")
            standardized["noi_usd"] = None
        else:
            try:
                noi_val = float(str(raw_noi).replace(",", "").replace("$", ""))
                if noi_val < 0:
                    warnings.append(f"noi is negative ({noi_val}); verify this is intentional.")
                standardized["noi_usd"] = round(noi_val, 2)
                fields_mapped += 1
            except (ValueError, TypeError):
                warnings.append(f"Cannot parse noi value: '{raw_noi}'. Set to null.")
                standardized["noi_usd"] = None

        # --- cap_rate ---
        raw_cap = _resolve("cap_rate")
        if raw_cap is None:
            warnings.append("Missing field: cap_rate.")
            standardized["cap_rate_decimal"] = None
        else:
            try:
                cap_val = float(str(raw_cap).replace("%", "").strip())
                # Normalize: if value > 1, assume it was given as a percentage
                if cap_val > 1.0:
                    cap_val = cap_val / 100.0
                if not (0.001 <= cap_val <= 0.30):
                    warnings.append(
                        f"cap_rate {cap_val:.4f} is outside typical range (0.1%–30%). "
                        "Verify input units."
                    )
                standardized["cap_rate_decimal"] = round(cap_val, 6)
                fields_mapped += 1
            except (ValueError, TypeError):
                warnings.append(f"Cannot parse cap_rate value: '{raw_cap}'. Set to null.")
                standardized["cap_rate_decimal"] = None

        # --- occupancy ---
        raw_occ = _resolve("occupancy")
        if raw_occ is None:
            warnings.append("Missing field: occupancy.")
            standardized["occupancy_decimal"] = None
        else:
            try:
                occ_val = float(str(raw_occ).replace("%", "").strip())
                # Normalize: if > 1, given as percentage
                if occ_val > 1.0:
                    occ_val = occ_val / 100.0
                if not (0.0 <= occ_val <= 1.0):
                    warnings.append(
                        f"occupancy {occ_val:.4f} is outside [0, 1] range after normalization."
                    )
                    occ_val = max(0.0, min(1.0, occ_val))
                standardized["occupancy_decimal"] = round(occ_val, 6)
                standardized["occupancy_pct"] = round(occ_val * 100, 2)
                fields_mapped += 1
            except (ValueError, TypeError):
                warnings.append(f"Cannot parse occupancy value: '{raw_occ}'. Set to null.")
                standardized["occupancy_decimal"] = None
                standardized["occupancy_pct"] = None

        # --- lease_expiry_schedule ---
        raw_schedule = _resolve("lease_expiry_schedule")
        if raw_schedule is None:
            warnings.append("Missing field: lease_expiry_schedule.")
            standardized["lease_expiry_schedule"] = []
        elif isinstance(raw_schedule, list):
            parsed_leases: list[dict] = []
            for idx, lease in enumerate(raw_schedule):
                if isinstance(lease, dict):
                    # Normalize common Argus lease dict fields
                    normalized_lease = {
                        "tenant":          str(lease.get("tenant", lease.get("Tenant", f"Tenant_{idx}"))),
                        "expiry_date":     str(lease.get("expiry_date", lease.get("Expiry", lease.get("expiration", "")))),
                        "sf":              _safe_float(lease.get("sf", lease.get("sqft", lease.get("area", None))), warnings, f"lease[{idx}].sf"),
                        "annual_rent":     _safe_float(lease.get("annual_rent", lease.get("rent", None)), warnings, f"lease[{idx}].annual_rent"),
                    }
                    parsed_leases.append(normalized_lease)
                else:
                    warnings.append(f"lease_expiry_schedule[{idx}] is not a dict; skipped.")
            standardized["lease_expiry_schedule"] = parsed_leases
            fields_mapped += 1
        elif isinstance(raw_schedule, str):
            warnings.append(
                "lease_expiry_schedule provided as raw string; stored as-is under "
                "'lease_expiry_schedule_raw'. Manual parsing required."
            )
            standardized["lease_expiry_schedule"] = []
            standardized["lease_expiry_schedule_raw"] = raw_schedule
        else:
            warnings.append(
                f"lease_expiry_schedule has unexpected type {type(raw_schedule).__name__}; stored as-is."
            )
            standardized["lease_expiry_schedule"] = []

        # --- Derived: implied_value ---
        if standardized.get("noi_usd") and standardized.get("cap_rate_decimal"):
            try:
                implied_value = standardized["noi_usd"] / standardized["cap_rate_decimal"]
                standardized["implied_property_value_usd"] = round(implied_value, 2)
            except ZeroDivisionError:
                warnings.append("cap_rate_decimal is zero; cannot compute implied_property_value.")

        # Report unrecognized passthrough fields
        for unk in sorted(unrecognized_fields):
            warnings.append(f"Unrecognized field '{unk}' passed through without mapping.")
            standardized[f"_passthrough_{unk}"] = argus_data[unk]

        # Metadata
        standardized["_schema_version"] = "1.0"
        standardized["_transformed_at"] = datetime.now(timezone.utc).isoformat()

        logger.info(
            "argus_to_json_transformer: %d fields mapped, %d warnings",
            fields_mapped, len(warnings)
        )

        return {
            "status": "success",
            "data": {
                "standardized_json": standardized,
                "fields_mapped": fields_mapped,
                "warnings": warnings
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("argus_to_json_transformer failed: %s", e)
        _log_lesson(f"argus_to_json_transformer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _safe_float(value: Any, warnings: list[str], field_label: str) -> float | None:
    """Coerce a value to float or append a warning and return None.

    Args:
        value: Raw value to coerce.
        warnings: List to append warning messages to.
        field_label: Human-readable label for the field (used in warning text).

    Returns:
        Coerced float or None if coercion fails.
    """
    if value is None:
        return None
    try:
        return float(str(value).replace(",", "").replace("$", "").strip())
    except (ValueError, TypeError):
        warnings.append(f"Cannot parse {field_label} value: '{value}'. Set to null.")
        return None


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
