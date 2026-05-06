---
skill: fcf_quality_analyzer
category: financial_analysis
description: Compares free cash flow to net income and highlights working capital effects.
tier: free
inputs: net_income, operating_cash_flow, capex, depreciation, stock_comp, change_in_receivables, change_in_payables, change_in_inventory
---

# Fcf Quality Analyzer

## Description
Compares free cash flow to net income and highlights working capital effects.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes |  |
| `operating_cash_flow` | `number` | Yes |  |
| `capex` | `number` | Yes |  |
| `depreciation` | `number` | Yes |  |
| `stock_comp` | `number` | Yes |  |
| `change_in_receivables` | `number` | Yes |  |
| `change_in_payables` | `number` | Yes |  |
| `change_in_inventory` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fcf_quality_analyzer",
  "arguments": {
    "net_income": 0,
    "operating_cash_flow": 0,
    "capex": 0,
    "depreciation": 0,
    "stock_comp": 0,
    "change_in_receivables": 0,
    "change_in_payables": 0,
    "change_in_inventory": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fcf_quality_analyzer"`.
