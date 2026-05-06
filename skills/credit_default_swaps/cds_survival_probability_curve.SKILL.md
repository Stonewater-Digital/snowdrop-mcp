---
skill: cds_survival_probability_curve
category: credit_default_swaps
description: Generates survival probabilities from hazard rates and tenors.
tier: free
inputs: hazard_rates, tenors_years
---

# Cds Survival Probability Curve

## Description
Generates survival probabilities from hazard rates and tenors.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hazard_rates` | `array` | Yes |  |
| `tenors_years` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_survival_probability_curve",
  "arguments": {
    "hazard_rates": [],
    "tenors_years": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_survival_probability_curve"`.
