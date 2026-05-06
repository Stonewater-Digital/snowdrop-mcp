---
skill: argus_to_json_transformer
category: real_estate
description: Transforms legacy Argus-style raw commercial real estate data dictionaries into a clean, standardized JSON schema with consistent field naming, type coercion, and a warnings list for missing or suspicious values.
tier: free
inputs: argus_data
---

# Argus To Json Transformer

## Description
Transforms legacy Argus-style raw commercial real estate data dictionaries into a clean, standardized JSON schema with consistent field naming, type coercion, and a warnings list for missing or suspicious values.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `argus_data` | `object` | Yes | Raw Argus export dict. Expected raw fields: property_name (str), noi (number), cap_rate (number), occupancy (number), lease_expiry_schedule (list of dicts or raw string). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "argus_to_json_transformer",
  "arguments": {
    "argus_data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "argus_to_json_transformer"`.
