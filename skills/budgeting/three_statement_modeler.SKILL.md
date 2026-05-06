---
skill: three_statement_modeler
category: budgeting
description: Generates linked financial statements using indirect cash flow method.
tier: free
inputs: income_statement, prior_balance_sheet, assumptions
---

# Three Statement Modeler

## Description
Generates linked financial statements using indirect cash flow method.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `income_statement` | `object` | Yes | Current-period income statement with fields: `revenue`, `cogs`, `operating_expenses`, `interest`, `tax_rate` (decimal, e.g. 0.25 = 25%). All monetary values in USD. |
| `prior_balance_sheet` | `object` | Yes | Prior-period ending balance sheet with fields: `cash`, `receivables`, `payables`, `debt`, `equity`, `other_assets`. All USD values. Used as starting point for cash flow and balance sheet projection. |
| `assumptions` | `object` | Yes | Working capital and financing assumptions: `days_receivable` (integer, collection days), `days_payable` (integer, payable days), `capex` (number, USD capital expenditures), `debt_repayment` (number, USD debt principal repaid). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

Data contains linked `income_statement`, `cash_flow_statement`, and `balance_sheet` objects, plus a `balanced` boolean confirming assets = liabilities + equity.

## Example
```json
{
  "tool": "three_statement_modeler",
  "arguments": {
    "income_statement": {
      "revenue": 120000,
      "cogs": 45000,
      "operating_expenses": 30000,
      "interest": 2000,
      "tax_rate": 0.25
    },
    "prior_balance_sheet": {
      "cash": 15000,
      "receivables": 12000,
      "payables": 8000,
      "debt": 50000,
      "equity": 80000,
      "other_assets": 5000
    },
    "assumptions": {
      "days_receivable": 30,
      "days_payable": 30,
      "capex": 10000,
      "debt_repayment": 5000
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "three_statement_modeler"`.
