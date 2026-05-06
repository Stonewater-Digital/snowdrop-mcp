---
skill: rwa_real_estate_parcel_zoning_attestor
category: crypto_rwa
description: Confirms each parcel's zoning class via municipal APIs to enforce token-level use restrictions.
tier: free
inputs: payload
---

# Rwa Real Estate Parcel Zoning Attestor

## Description
Confirms each parcel's zoning class via municipal APIs to enforce token-level use restrictions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_parcel_zoning_attestor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_parcel_zoning_attestor"`.
