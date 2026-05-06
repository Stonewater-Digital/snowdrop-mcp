---
skill: dpi_calculator
category: fund_admin
description: Calculates DPI (Distributions to Paid-In) = cumulative_distributions / paid_in_capital. DPI is the realized component of fund performance — cash actually returned to LPs.
tier: premium
inputs: cumulative_distributions, paid_in_capital
---

# Dpi Calculator

## Description
Calculates DPI (Distributions to Paid-In) = cumulative_distributions / paid_in_capital. DPI is the realized component of fund performance — cash actually returned to LPs. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| cumulative_distributions | number | Yes | Total cash distributions returned to LPs since fund inception (USD) |
| paid_in_capital | number | Yes | Total LP capital called and contributed to the fund (USD) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dpi_calculator",
  "arguments": {
    "cumulative_distributions": 42000000,
    "paid_in_capital": 60000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dpi_calculator"`.
