---
skill: pain_ratio_calculator
category: market_analytics
description: Computes the Pain Index (average drawdown magnitude) and Pain Ratio (return/Pain).
tier: free
inputs: prices
---

# Pain Ratio Calculator

## Description
Computes the Pain Index (average drawdown magnitude) and Pain Ratio (return/Pain).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Equity curve or NAV series. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pain_ratio_calculator",
  "arguments": {
    "prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pain_ratio_calculator"`.
