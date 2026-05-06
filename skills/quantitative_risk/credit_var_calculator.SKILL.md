---
skill: credit_var_calculator
category: quantitative_risk
description: CreditMetrics style credit VaR computing conditional default probabilities and obligor contributions.
tier: free
inputs: obligor_ratings, transition_matrix, exposures, lgd_pct, asset_correlations
---

# Credit Var Calculator

## Description
CreditMetrics style credit VaR computing conditional default probabilities and obligor contributions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `obligor_ratings` | `array` | Yes | List of current ratings (e.g., AAA, BBB, Default) for each obligor. |
| `transition_matrix` | `object` | Yes | Mapping of rating to probabilities of transitioning to other ratings including 'Default'. |
| `exposures` | `array` | Yes | Exposure at default (EAD) for each obligor in base currency. |
| `lgd_pct` | `array` | Yes | Loss-given-default percentages per obligor (0-100). |
| `asset_correlations` | `array` | Yes | Asset correlations (rho) for each obligor vs systematic factor per Basel IRB guidance. |
| `confidence_level` | `number` | No | Confidence level for quantile, default 0.999 for credit portfolios. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_var_calculator",
  "arguments": {
    "obligor_ratings": [],
    "transition_matrix": {},
    "exposures": [],
    "lgd_pct": [],
    "asset_correlations": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_var_calculator"`.
