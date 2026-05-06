---
skill: expense_allocation_engine
category: fund_accounting
description: Distributes fund expenses across share classes according to commitment or NAV weights. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Expense Allocation Engine

## Description
Distributes fund expenses across share classes according to commitment or NAV weights. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "expense_allocation_engine",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "expense_allocation_engine"`.
