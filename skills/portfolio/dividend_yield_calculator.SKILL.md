---
skill: dividend_yield_calculator
category: portfolio
description: Calculates the dividend yield as a percentage of the current stock price.
tier: free
inputs: annual_dividend, stock_price
---

# Dividend Yield Calculator

## Description
Calculates the dividend yield as a percentage of the current stock price.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_dividend` | `number` | Yes | Total annual dividend per share. |
| `stock_price` | `number` | Yes | Current stock price per share. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dividend_yield_calculator",
  "arguments": {
    "annual_dividend": 0,
    "stock_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dividend_yield_calculator"`.
