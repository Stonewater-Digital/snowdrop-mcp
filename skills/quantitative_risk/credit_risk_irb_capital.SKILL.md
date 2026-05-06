---
skill: credit_risk_irb_capital
category: quantitative_risk
description: Applies Basel IRB corporate formula for rho, maturity adjustment, and capital (K).
tier: free
inputs: pd_list, lgd_list, ead_list, maturities
---

# Credit Risk Irb Capital

## Description
Applies Basel IRB corporate formula for rho, maturity adjustment, and capital (K).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pd_list` | `array` | Yes | Probability of default per obligor (decimals). |
| `lgd_list` | `array` | Yes | Loss-given-default percentages per obligor. |
| `ead_list` | `array` | Yes | Exposure at default per obligor. |
| `maturities` | `array` | Yes | Effective maturity in years (M). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_risk_irb_capital",
  "arguments": {
    "pd_list": [],
    "lgd_list": [],
    "ead_list": [],
    "maturities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_risk_irb_capital"`.
