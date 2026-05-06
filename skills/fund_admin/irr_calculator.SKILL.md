---
skill: irr_calculator
category: fund_admin
description: Computes IRR via Newton-Raphson iteration for periodic cash flows. Requires at least one sign change in the cash flow series.
tier: premium
inputs: none
---

# Irr Calculator

## Description
Computes IRR via Newton-Raphson iteration for periodic cash flows. Requires at least one sign change in the cash flow series. Returns IRR as an annualized percentage. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "irr_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "irr_calculator"`.
