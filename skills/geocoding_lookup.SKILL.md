---
skill: geocoding_lookup
category: root
description: Google Geocoding API skill for address normalization, coordinate lookup, address validation, and timezone resolution. Used in real estate and location-based financial analysis pipelines.
tier: free
inputs: action
---

# Geocoding Lookup

## Description
Google Geocoding API skill for address normalization, coordinate lookup, address validation, and timezone resolution. Used in real estate and location-based financial analysis pipelines.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | The geocoding operation to perform. |
| `address` | `string` | No | Street address string (required for geocode and validate). |
| `latitude` | `number` | No | Decimal latitude (required for reverse_geocode and timezone). |
| `longitude` | `number` | No | Decimal longitude (required for reverse_geocode and timezone). |
| `language` | `string` | No | BCP-47 language tag for API response localization. |
| `region` | `string` | No | CLDR region code to bias geocoding results (e.g. 'us'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "geocoding_lookup",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "geocoding_lookup"`.
