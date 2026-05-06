---
skill: downside_risk_metrics
category: market_analytics
description: Computes downside deviation, upside potential ratio, gain/loss ratio, and Bernardo-Ledoit ratio.
tier: free
inputs: returns, mar
---

# Downside Risk Metrics

## Description
Computes downside deviation, upside potential ratio, gain/loss ratio, and Bernardo-Ledoit ratio.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Return series. |
| `mar` | `number` | Yes | Minimum acceptable return (MAR). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "downside_risk_metrics",
  "arguments": {
    "returns": [],
    "mar": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "downside_risk_metrics"`.
