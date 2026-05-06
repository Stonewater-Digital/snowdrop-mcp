---
skill: risk_parity_allocator
category: alternative_investments
description: Uses iterative proportional fitting on the covariance matrix to achieve target risk budgets per asset. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: covariance_matrix, risk_budgets
---

# Risk Parity Allocator

## Description
Uses iterative proportional fitting on the covariance matrix to produce portfolio weights that achieve target risk budget contributions per asset. Supports equal risk contribution and custom risk budget specifications. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `covariance_matrix` | `array` | Yes | N×N covariance matrix as a 2D list of lists (annualized). |
| `risk_budgets` | `array` | Yes | Target risk budget fractions per asset (must sum to 1.0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "risk_parity_allocator",
  "arguments": {
    "covariance_matrix": [
      [0.04, 0.01, 0.005],
      [0.01, 0.09, 0.012],
      [0.005, 0.012, 0.025]
    ],
    "risk_budgets": [0.33, 0.33, 0.34]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_parity_allocator"`.
