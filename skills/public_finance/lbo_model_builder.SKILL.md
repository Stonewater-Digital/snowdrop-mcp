---
skill: lbo_model_builder
category: public_finance
description: Models leverage, cash flows, and equity returns for a stylized LBO.
tier: free
inputs: purchase_price, ebitda, debt_tranches, equity_contribution, ebitda_growth_rate, exit_multiple, capex_pct_revenue, working_capital_pct_revenue
---

# Lbo Model Builder

## Description
Models leverage, cash flows, and equity returns for a stylized LBO.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purchase_price` | `number` | Yes |  |
| `ebitda` | `number` | Yes |  |
| `debt_tranches` | `array` | Yes |  |
| `equity_contribution` | `number` | Yes |  |
| `ebitda_growth_rate` | `number` | Yes |  |
| `exit_multiple` | `number` | Yes |  |
| `hold_period_years` | `integer` | No |  |
| `capex_pct_revenue` | `number` | Yes |  |
| `working_capital_pct_revenue` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lbo_model_builder",
  "arguments": {
    "purchase_price": 0,
    "ebitda": 0,
    "debt_tranches": [],
    "equity_contribution": 0,
    "ebitda_growth_rate": 0,
    "exit_multiple": 0,
    "capex_pct_revenue": 0,
    "working_capital_pct_revenue": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lbo_model_builder"`.
