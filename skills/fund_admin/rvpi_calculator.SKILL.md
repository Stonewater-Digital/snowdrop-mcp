---
skill: rvpi_calculator
category: fund_admin
description: Calculates RVPI (Residual Value to Paid-In) = residual_value / paid_in_capital. RVPI is the unrealized component of fund value — what the portfolio is still worth.
tier: premium
inputs: residual_value, paid_in_capital
---

# Rvpi Calculator

## Description
Calculates RVPI (Residual Value to Paid-In) = residual_value / paid_in_capital. RVPI is the unrealized component of fund value — what the portfolio is still worth. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| residual_value | number | Yes | Current fair value of all remaining unrealized portfolio positions (NAV, USD) |
| paid_in_capital | number | Yes | Total LP capital called and contributed to the fund to date (USD) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rvpi_calculator",
  "arguments": {
    "residual_value": 68000000,
    "paid_in_capital": 55000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rvpi_calculator"`.
