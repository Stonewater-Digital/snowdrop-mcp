---
skill: earnings_surprise_calculator
category: market_analytics
description: Calculates EPS surprise percentage, SUE proxy, and price-drift implications (PEAD).
tier: free
inputs: actual_eps, consensus_estimate, stock_price_before, stock_price_after
---

# Earnings Surprise Calculator

## Description
Calculates EPS surprise percentage, SUE proxy, and price-drift implications (PEAD).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `actual_eps` | `number` | Yes | Reported EPS. |
| `consensus_estimate` | `number` | Yes | Consensus EPS estimate. |
| `stock_price_before` | `number` | Yes | Price before earnings. |
| `stock_price_after` | `number` | Yes | Price after earnings. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "earnings_surprise_calculator",
  "arguments": {
    "actual_eps": 0,
    "consensus_estimate": 0,
    "stock_price_before": 0,
    "stock_price_after": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earnings_surprise_calculator"`.
