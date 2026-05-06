---
skill: fund_expense_allocator
category: fund_accounting
description: Allocates a total expense amount across sub-funds based on their chosen allocation basis: 'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or 'committed_capital' (weighted by LP capital commitments). Returns dollar allocations and percentage shares for each sub-fund.
tier: premium
inputs: none
---

# Fund Expense Allocator

## Description
Allocates a total expense amount across sub-funds based on their chosen allocation basis: 'pro_rata_nav' (weighted by current NAV), 'equal' (split evenly), or 'committed_capital' (weighted by LP capital commitments). Returns dollar allocations and percentage shares for each sub-fund. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fund_expense_allocator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_expense_allocator"`.
