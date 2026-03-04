"""
Executive Summary: Analyzes parcel density rules to determine max buildable units and compliance with proposed use.
Inputs: parcel_data (dict: parcel_id, lot_size_sqft, current_zoning, proposed_use), zoning_rules (dict: allowed_density_units_per_acre, max_height_ft, setback_ft, parking_ratio)
Outputs: dict with allowed_density (float), max_units (int), restrictions (list), compliant (bool)
MCP Tool Name: zoning_impact_analyzer
"""
import os
import logging
import math
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "zoning_impact_analyzer",
    "description": (
        "Analyzes parcel zoning rules to determine maximum buildable density, "
        "parking requirements, and compliance of a proposed land use. "
        "Returns restriction list and compliant flag."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "parcel_data": {
                "type": "object",
                "description": "Parcel characteristics.",
                "properties": {
                    "parcel_id":       {"type": "string"},
                    "lot_size_sqft":   {"type": "number"},
                    "current_zoning":  {"type": "string"},
                    "proposed_use":    {"type": "string"}
                },
                "required": ["parcel_id", "lot_size_sqft", "current_zoning", "proposed_use"]
            },
            "zoning_rules": {
                "type": "object",
                "description": "Applicable zoning code parameters.",
                "properties": {
                    "allowed_density_units_per_acre": {"type": "number"},
                    "max_height_ft":                 {"type": "number"},
                    "setback_ft":                    {"type": "number"},
                    "parking_ratio":                 {"type": "number", "description": "Spaces per unit."}
                },
                "required": ["allowed_density_units_per_acre"]
            }
        },
        "required": ["parcel_data", "zoning_rules"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "allowed_density":  {"type": "number"},
                    "max_units":        {"type": "integer"},
                    "restrictions":     {"type": "array"},
                    "compliant":        {"type": "boolean"},
                    "required_parking": {"type": "number"}
                },
                "required": ["allowed_density", "max_units", "restrictions", "compliant"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

SQFT_PER_ACRE: float = 43_560.0

# Simple allowed-use compatibility table (extendable)
USE_COMPATIBILITY: dict[str, list[str]] = {
    "R1":  ["single_family", "residential"],
    "R2":  ["single_family", "duplex", "residential"],
    "R3":  ["multifamily", "apartment", "residential", "condo"],
    "R4":  ["multifamily", "apartment", "residential", "condo", "mixed_use"],
    "C1":  ["retail", "office", "commercial", "mixed_use"],
    "C2":  ["retail", "office", "commercial", "mixed_use", "industrial_light"],
    "M1":  ["industrial_light", "warehouse", "flex"],
    "M2":  ["industrial", "industrial_light", "warehouse", "manufacturing"],
    "MXD": ["multifamily", "retail", "office", "commercial", "mixed_use", "residential"],
}


def zoning_impact_analyzer(
    parcel_data: dict,
    zoning_rules: dict,
    **kwargs: Any
) -> dict:
    """Analyze parcel zoning to compute max buildable units and compliance.

    Converts lot size from square feet to acres, applies density rules to compute
    maximum units, calculates required parking, and checks proposed use against
    the current zoning district's allowed uses.

    Args:
        parcel_data: Dict with parcel_id (str), lot_size_sqft (float),
            current_zoning (str), proposed_use (str).
        zoning_rules: Dict with allowed_density_units_per_acre (float, required),
            max_height_ft (float, optional), setback_ft (float, optional),
            parking_ratio (float, optional, spaces per unit).
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (allowed_density, max_units, restrictions,
        compliant, required_parking, lot_acres, parcel_id), timestamp.

    Raises:
        ValueError: If required fields are missing or lot_size_sqft is non-positive.
    """
    try:
        # Validate parcel_data
        required_parcel = ["parcel_id", "lot_size_sqft", "current_zoning", "proposed_use"]
        for field in required_parcel:
            if field not in parcel_data:
                raise ValueError(f"parcel_data missing required field '{field}'.")

        parcel_id: str = str(parcel_data["parcel_id"])
        lot_size_sqft: float = float(parcel_data["lot_size_sqft"])
        current_zoning: str = str(parcel_data["current_zoning"]).upper().strip()
        proposed_use: str = str(parcel_data["proposed_use"]).lower().strip().replace(" ", "_")

        if lot_size_sqft <= 0:
            raise ValueError(f"lot_size_sqft must be positive, got {lot_size_sqft}")

        # Validate zoning_rules
        if "allowed_density_units_per_acre" not in zoning_rules:
            raise ValueError("zoning_rules missing required field 'allowed_density_units_per_acre'.")

        density_per_acre: float = float(zoning_rules["allowed_density_units_per_acre"])
        max_height_ft: float | None = (
            float(zoning_rules["max_height_ft"]) if "max_height_ft" in zoning_rules else None
        )
        setback_ft: float | None = (
            float(zoning_rules["setback_ft"]) if "setback_ft" in zoning_rules else None
        )
        parking_ratio: float | None = (
            float(zoning_rules["parking_ratio"]) if "parking_ratio" in zoning_rules else None
        )

        restrictions: list[str] = []

        # Compute lot in acres and max buildable units
        lot_acres: float = lot_size_sqft / SQFT_PER_ACRE
        allowed_density: float = round(density_per_acre * lot_acres, 4)
        max_units: int = math.floor(allowed_density)

        if max_units < 1:
            restrictions.append(
                f"Lot size of {lot_acres:.3f} acres at {density_per_acre} units/acre "
                f"yields {allowed_density:.3f} units — less than 1 buildable unit."
            )

        # Parking requirement
        required_parking: float | None = None
        if parking_ratio is not None and max_units > 0:
            required_parking = round(parking_ratio * max_units, 1)

        # Height restriction note
        if max_height_ft is not None:
            restrictions.append(f"Maximum building height: {max_height_ft} ft.")

        # Setback restriction note
        if setback_ft is not None:
            restrictions.append(f"Required setback: {setback_ft} ft on all sides.")

        # Use compatibility check
        compliant: bool = True
        allowed_uses = USE_COMPATIBILITY.get(current_zoning, [])
        if allowed_uses:
            # Check if proposed use matches any allowed use (substring match for flexibility)
            use_allowed = any(
                proposed_use == allowed or proposed_use in allowed or allowed in proposed_use
                for allowed in allowed_uses
            )
            if not use_allowed:
                compliant = False
                restrictions.append(
                    f"Proposed use '{proposed_use}' is NOT permitted in zone '{current_zoning}'. "
                    f"Allowed uses: {', '.join(allowed_uses)}."
                )
        else:
            restrictions.append(
                f"Zone '{current_zoning}' not found in local compatibility table. "
                "Manual zoning review required."
            )
            # Cannot confirm compliance without known rules
            compliant = False

        # Density-based restrictions
        if density_per_acre > 50:
            restrictions.append(
                f"High-density zoning ({density_per_acre} units/acre) — "
                "environmental impact and infrastructure capacity review recommended."
            )

        result: dict = {
            "parcel_id": parcel_id,
            "lot_size_sqft": lot_size_sqft,
            "lot_acres": round(lot_acres, 4),
            "current_zoning": current_zoning,
            "proposed_use": proposed_use,
            "allowed_density": allowed_density,
            "max_units": max_units,
            "restrictions": restrictions,
            "compliant": compliant,
        }

        if required_parking is not None:
            result["required_parking_spaces"] = required_parking
            result["parking_ratio_per_unit"] = parking_ratio
        if max_height_ft is not None:
            result["max_height_ft"] = max_height_ft
        if setback_ft is not None:
            result["setback_ft"] = setback_ft

        logger.info(
            "zoning_impact_analyzer: parcel=%s, max_units=%d, compliant=%s",
            parcel_id, max_units, compliant
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("zoning_impact_analyzer failed: %s", e)
        _log_lesson(f"zoning_impact_analyzer: {e}")
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
