---
skill: rwa_real_estate_occupancy_certificate_validator
category: crypto_rwa
description: Verifies certificates of occupancy and permit status for new developments.
tier: free
inputs: payload
---

# Rwa Real Estate Occupancy Certificate Validator

## Description
Verifies certificates of occupancy and permit status for new developments.

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
  "tool": "rwa_real_estate_occupancy_certificate_validator",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_occupancy_certificate_validator"`.
