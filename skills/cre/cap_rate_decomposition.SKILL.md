---
skill: cap_rate_decomposition
category: cre
description: Breaks down cap rate into risk-free, property, market, and vacancy components.
tier: free
inputs: cap_rate, risk_free_rate, property_type, market_tier, building_class, occupancy_pct
---

# Cap Rate Decomposition

## Description
Breaks down cap rate into risk-free, property, market, and vacancy components.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cap_rate` | `number` | Yes |  |
| `risk_free_rate` | `number` | Yes |  |
| `property_type` | `string` | Yes |  |
| `market_tier` | `string` | Yes |  |
| `building_class` | `string` | Yes |  |
| `occupancy_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cap_rate_decomposition",
  "arguments": {
    "cap_rate": 0,
    "risk_free_rate": 0,
    "property_type": "<property_type>",
    "market_tier": "<market_tier>",
    "building_class": "<building_class>",
    "occupancy_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cap_rate_decomposition"`.
