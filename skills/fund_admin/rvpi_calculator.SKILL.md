---
skill: rvpi_calculator
category: fund_admin
description: Calculates RVPI (Residual Value to Paid-In) = residual_value / paid_in_capital. RVPI is the unrealized component of fund value — what the portfolio is still worth.
tier: premium
inputs: none
---

# Rvpi Calculator

## Description
Calculates RVPI (Residual Value to Paid-In) = residual_value / paid_in_capital. RVPI is the unrealized component of fund value — what the portfolio is still worth. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rvpi_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rvpi_calculator"`.
