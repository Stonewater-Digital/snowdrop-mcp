---
skill: cross_rate_calculator
category: fx
description: Calculate a cross exchange rate from two USD-based rates. cross_rate = base_usd_rate / quote_usd_rate.
tier: free
inputs: base_usd_rate, quote_usd_rate
---

# Cross Rate Calculator

## Description
Calculate a cross exchange rate from two USD-based rates. cross_rate = base_usd_rate / quote_usd_rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_usd_rate` | `number` | Yes | USD rate for the base currency (e.g. EUR/USD = 1.08 means 1 EUR = 1.08 USD). |
| `quote_usd_rate` | `number` | Yes | USD rate for the quote currency (e.g. GBP/USD = 1.27 means 1 GBP = 1.27 USD). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cross_rate_calculator",
  "arguments": {
    "base_usd_rate": 0,
    "quote_usd_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cross_rate_calculator"`.
