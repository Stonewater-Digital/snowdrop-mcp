---
skill: fund_expense_allocator
category: fund_admin
description: Allocates fund-level expenses to LP capital accounts on a pro-rata basis using each LP's relative balance weight. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Fund Expense Allocator

## Description
Allocates fund-level expenses to LP capital accounts on a pro-rata basis using each LP's relative balance weight. (Premium — subscribe at https://snowdrop.ai)

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
