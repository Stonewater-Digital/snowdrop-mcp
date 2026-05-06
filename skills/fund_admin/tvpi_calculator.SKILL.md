---
skill: tvpi_calculator
category: fund_admin
description: Calculates TVPI (Total Value to Paid-In) = (DPI + RVPI). TVPI = (cumulative_distributions + residual_value) / paid_in_capital.
tier: premium
inputs: residual_value, cumulative_distributions, paid_in_capital
---

# Tvpi Calculator

## Description
Calculates TVPI (Total Value to Paid-In) = (DPI + RVPI). TVPI = (cumulative_distributions + residual_value) / paid_in_capital. Also reports DPI, RVPI, and NAV share. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| residual_value | number | Yes | Current fair value of remaining unrealized portfolio positions (NAV, USD) |
| cumulative_distributions | number | Yes | Total cash distributions returned to LPs since inception (USD) |
| paid_in_capital | number | Yes | Total LP capital called and contributed to the fund (USD) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tvpi_calculator",
  "arguments": {
    "residual_value": 52000000,
    "cumulative_distributions": 38000000,
    "paid_in_capital": 60000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tvpi_calculator"`.
