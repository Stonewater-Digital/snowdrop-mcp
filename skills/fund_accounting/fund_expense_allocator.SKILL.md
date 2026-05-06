---
skill: fund_expense_allocator
category: fund_accounting
description: Allocates a total expense amount across sub-funds based on their chosen allocation basis: 'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or 'committed_capital' (weighted by LP capital commitments). Returns dollar allocations and percentage shares for each sub-fund.
tier: premium
inputs: total_expenses, sub_funds
---

# Fund Expense Allocator

## Description
Allocates a total expense amount across sub-funds based on their chosen allocation basis: 'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or 'committed_capital' (weighted by LP capital commitments). Returns dollar allocations and percentage shares for each sub-fund. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_expenses` | `number` | Yes | Total expense amount to be allocated across sub-funds in dollars. |
| `sub_funds` | `array` | Yes | List of sub-fund objects, each with `name`, `nav`, `committed_capital`, and `allocation_basis` (one of `"pro_rata_nav"`, `"equal"`, `"committed_capital"`). |

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
    "total_expenses": 250000,
    "sub_funds": [
      {"name": "Fund I", "nav": 45000000, "committed_capital": 50000000, "allocation_basis": "pro_rata_nav"},
      {"name": "Fund II", "nav": 30000000, "committed_capital": 35000000, "allocation_basis": "pro_rata_nav"},
      {"name": "Co-Invest SPV", "nav": 10000000, "committed_capital": 10000000, "allocation_basis": "pro_rata_nav"}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_expense_allocator"`.
