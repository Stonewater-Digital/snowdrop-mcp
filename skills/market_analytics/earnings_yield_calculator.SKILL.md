---
skill: earnings_yield_calculator
category: market_analytics
description: Computes earnings yield (inverse P/E) and compares against the 10Y Treasury yield.
tier: free
inputs: eps, stock_price, treasury_10yr_yield
---

# Earnings Yield Calculator

## Description
Computes earnings yield (inverse P/E) and compares against the 10Y Treasury yield.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `eps` | `number` | Yes | Earnings per share. |
| `stock_price` | `number` | Yes | Current share price. |
| `treasury_10yr_yield` | `number` | Yes | 10-year Treasury yield (decimal). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "earnings_yield_calculator",
  "arguments": {
    "eps": 0,
    "stock_price": 0,
    "treasury_10yr_yield": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earnings_yield_calculator"`.
