---
skill: tif_district_calculator
category: muni_finance
description: Projects increment revenue and coverage for TIF districts over the term.
tier: free
inputs: base_assessed_value, projected_assessed_value, tax_rate_per_100, tif_term_years, project_cost
---

# Tif District Calculator

## Description
Projects increment revenue and coverage for TIF districts over the term.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_assessed_value` | `number` | Yes |  |
| `projected_assessed_value` | `number` | Yes |  |
| `tax_rate_per_100` | `number` | Yes |  |
| `tif_term_years` | `integer` | Yes |  |
| `project_cost` | `number` | Yes |  |
| `annual_growth_rate` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tif_district_calculator",
  "arguments": {
    "base_assessed_value": 0,
    "projected_assessed_value": 0,
    "tax_rate_per_100": 0,
    "tif_term_years": 0,
    "project_cost": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tif_district_calculator"`.
