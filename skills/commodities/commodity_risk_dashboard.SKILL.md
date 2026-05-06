---
skill: commodity_risk_dashboard
category: commodities
description: Aggregates gross/net notional, parametric 1-day 95% VaR per position, portfolio VaR proxy, oil-beta weighted exposure, and concentration flags.
tier: free
inputs: positions
---

# Commodity Risk Dashboard

## Description
Aggregates gross/net notional, parametric 1-day 95% VaR per position, portfolio VaR proxy, oil-beta weighted exposure, and concentration flags.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes | List of commodity positions. |
| `confidence_level` | `number` | No | Z-score for VaR confidence level (1.645 = 95%, 2.326 = 99%). Defaults to 1.645. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commodity_risk_dashboard",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_risk_dashboard"`.
