---
skill: value_at_risk_parametric
category: market_analytics
description: Computes Gaussian VaR and expected shortfall over a specified horizon.
tier: free
inputs: returns, confidence_level, horizon_days
---

# Value At Risk Parametric

## Description
Computes Gaussian VaR and expected shortfall over a specified horizon.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Historical returns (decimal). |
| `confidence_level` | `number` | Yes | Confidence level between 0 and 1. |
| `horizon_days` | `integer` | Yes | VaR horizon in days. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "value_at_risk_parametric",
  "arguments": {
    "returns": [],
    "confidence_level": 0,
    "horizon_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "value_at_risk_parametric"`.
