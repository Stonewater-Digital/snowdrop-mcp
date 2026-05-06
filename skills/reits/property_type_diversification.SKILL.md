---
skill: property_type_diversification
category: reits
description: Computes HHI concentration and highlights overweight property types.
tier: free
inputs: property_mix
---

# Property Type Diversification

## Description
Computes HHI concentration and highlights overweight property types.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `property_mix` | `array` | Yes |  |
| `limit_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "property_type_diversification",
  "arguments": {
    "property_mix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "property_type_diversification"`.
