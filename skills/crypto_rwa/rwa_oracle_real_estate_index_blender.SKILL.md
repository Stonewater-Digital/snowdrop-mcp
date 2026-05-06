---
skill: rwa_oracle_real_estate_index_blender
category: crypto_rwa
description: Blends Case-Shiller and proprietary comps to smooth real-estate NAV ticks feeding tokens.
tier: free
inputs: payload
---

# Rwa Oracle Real Estate Index Blender

## Description
Blends Case-Shiller and proprietary comps to smooth real-estate NAV ticks feeding tokens.

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
  "tool": "rwa_oracle_real_estate_index_blender",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_real_estate_index_blender"`.
