---
skill: counterparty_credit_charge
category: credit_derivatives
description: Computes bilateral credit adjustments (CVA/DVA) by integrating discounted exposures with marginal default probabilities per Basel CVA methodology.
tier: free
inputs: time_points_years, positive_exposures, negative_exposures, discount_factors, counterparty_default_probabilities, firm_default_probabilities, recovery_counterparty, recovery_firm
---

# Counterparty Credit Charge

## Description
Computes bilateral credit adjustments (CVA/DVA) by integrating discounted exposures with marginal default probabilities per Basel CVA methodology.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `time_points_years` | `array` | Yes | Future time buckets in years. |
| `positive_exposures` | `array` | Yes | Expected positive exposure (counterparty owes us) per bucket. |
| `negative_exposures` | `array` | Yes | Expected negative exposure (we owe counterparty) per bucket. |
| `discount_factors` | `array` | Yes | Risk-free discount factors per bucket. |
| `counterparty_default_probabilities` | `array` | Yes | Marginal default probabilities for the counterparty per bucket. |
| `firm_default_probabilities` | `array` | Yes | Marginal default probabilities for our firm per bucket (for DVA). |
| `recovery_counterparty` | `number` | Yes | Counterparty recovery rate. |
| `recovery_firm` | `number` | Yes | Our own recovery rate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "counterparty_credit_charge",
  "arguments": {
    "time_points_years": [],
    "positive_exposures": [],
    "negative_exposures": [],
    "discount_factors": [],
    "counterparty_default_probabilities": [],
    "firm_default_probabilities": [],
    "recovery_counterparty": 0,
    "recovery_firm": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "counterparty_credit_charge"`.
