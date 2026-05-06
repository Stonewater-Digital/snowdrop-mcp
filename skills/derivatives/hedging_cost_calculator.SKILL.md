---
skill: hedging_cost_calculator
category: derivatives
description: Quantifies hedging cost, downside, and upside caps across hedge types.
tier: free
inputs: position_value, hedge_type, hedge_params
---

# Hedging Cost Calculator

## Description
Quantifies hedging cost, downside, and upside caps across hedge types.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `position_value` | `number` | Yes |  |
| `hedge_type` | `string` | Yes |  |
| `hedge_params` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "hedging_cost_calculator",
  "arguments": {
    "position_value": 0,
    "hedge_type": "<hedge_type>",
    "hedge_params": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hedging_cost_calculator"`.
