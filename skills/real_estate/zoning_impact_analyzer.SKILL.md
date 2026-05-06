---
skill: zoning_impact_analyzer
category: real_estate
description: Analyzes parcel zoning rules to determine maximum buildable density, parking requirements, and compliance of a proposed land use. Returns restriction list and compliant flag.
tier: free
inputs: parcel_data, zoning_rules
---

# Zoning Impact Analyzer

## Description
Analyzes parcel zoning rules to determine maximum buildable density, parking requirements, and compliance of a proposed land use. Returns restriction list and compliant flag.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `parcel_data` | `object` | Yes | Parcel characteristics. |
| `zoning_rules` | `object` | Yes | Applicable zoning code parameters. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "zoning_impact_analyzer",
  "arguments": {
    "parcel_data": {},
    "zoning_rules": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "zoning_impact_analyzer"`.
