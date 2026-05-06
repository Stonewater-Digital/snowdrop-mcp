---
skill: capital_allocation_raroc
category: regulatory_capital
description: Calculates RAROC and economic value added per business line for regulatory capital planning.
tier: free
inputs: business_units, cost_of_capital_pct
---

# Capital Allocation Raroc

## Description
Calculates RAROC and economic value added per business line for regulatory capital planning.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `business_units` | `array` | Yes | Units with revenue, expected loss, and economic capital. |
| `cost_of_capital_pct` | `number` | Yes | Target cost of capital (hurdle rate). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_allocation_raroc",
  "arguments": {
    "business_units": [],
    "cost_of_capital_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_allocation_raroc"`.
