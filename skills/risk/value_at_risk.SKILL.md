---
skill: value_at_risk
category: risk
description: Computes multi-level VaR and CVaR via historical simulation.
tier: free
inputs: positions, holding_period_days
---

# Value At Risk

## Description
Computes multi-level VaR and CVaR via historical simulation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `confidence_levels` | `array` | No |  |
| `holding_period_days` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "value_at_risk",
  "arguments": {
    "positions": [],
    "holding_period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "value_at_risk"`.
