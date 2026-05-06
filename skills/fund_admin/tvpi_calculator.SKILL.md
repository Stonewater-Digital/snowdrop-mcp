---
skill: tvpi_calculator
category: fund_admin
description: Calculates TVPI (Total Value to Paid-In) = (DPI + RVPI). TVPI = (cumulative_distributions + residual_value) / paid_in_capital.
tier: premium
inputs: none
---

# Tvpi Calculator

## Description
Calculates TVPI (Total Value to Paid-In) = (DPI + RVPI). TVPI = (cumulative_distributions + residual_value) / paid_in_capital. Also reports DPI, RVPI, and NAV share. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "tvpi_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tvpi_calculator"`.
