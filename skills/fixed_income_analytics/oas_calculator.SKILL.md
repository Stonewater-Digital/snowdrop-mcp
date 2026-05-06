---
skill: oas_calculator
category: fixed_income_analytics
description: Calibrates a lognormal Black-Derman-Toy short-rate lattice to the supplied zero curve and derives the option-adjusted spread (OAS) required to reconcile the lattice price with the observed market price. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Oas Calculator

## Description
Calibrates a lognormal Black-Derman-Toy short-rate lattice to the supplied zero curve and derives the option-adjusted spread (OAS) required to reconcile the lattice price with the observed market price. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "oas_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "oas_calculator"`.
