---
skill: value_at_risk_historical
category: market_analytics
description: Computes historical VaR by sampling past returns and scaling by the desired horizon.
tier: free
inputs: returns, confidence_level, horizon_days
---

# Value At Risk Historical

## Description
Computes historical VaR by sampling past returns and scaling by the desired horizon.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Historical returns (decimal). |
| `confidence_level` | `number` | Yes | Confidence level (0-1). |
| `horizon_days` | `integer` | Yes | Holding period in days. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "value_at_risk_historical",
  "arguments": {
    "returns": [],
    "confidence_level": 0,
    "horizon_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "value_at_risk_historical"`.
