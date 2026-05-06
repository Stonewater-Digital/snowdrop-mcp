---
skill: dpi_calculator
category: fund_admin
description: Calculates DPI (Distributions to Paid-In) = cumulative_distributions / paid_in_capital. DPI is the realized component of fund performance — cash actually returned to LPs.
tier: premium
inputs: none
---

# Dpi Calculator

## Description
Calculates DPI (Distributions to Paid-In) = cumulative_distributions / paid_in_capital. DPI is the realized component of fund performance — cash actually returned to LPs. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "dpi_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dpi_calculator"`.
