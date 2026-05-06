---
skill: fund_expense_allocator
category: fund_admin
description: Allocates fund-level expenses to LP capital accounts on a pro-rata basis using each LP's relative balance weight. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: expense_amount, capital_accounts
---

# Fund Expense Allocator

## Description
Allocates fund-level expenses to LP capital accounts on a pro-rata basis using each LP's relative balance weight. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| expense_amount | number | Yes | Total fund-level expense to be allocated across all LP capital accounts (USD) |
| capital_accounts | array | Yes | List of LP capital account objects, each with `lp_name` (string) and `balance` (number) used to compute pro-rata weights |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fund_expense_allocator",
  "arguments": {
    "expense_amount": 125000,
    "capital_accounts": [
      {"lp_name": "Pension Fund Alpha", "balance": 8500000},
      {"lp_name": "Insurance Co Beta", "balance": 5000000},
      {"lp_name": "Family Office Gamma", "balance": 1500000}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_expense_allocator"`.
