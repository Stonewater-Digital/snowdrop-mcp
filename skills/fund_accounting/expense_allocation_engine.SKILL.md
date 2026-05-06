---
skill: expense_allocation_engine
category: fund_accounting
description: Distributes fund expenses across share classes according to commitment or NAV weights. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: expenses, share_classes, method
---

# Expense Allocation Engine

## Description
Distributes fund expenses across share classes according to commitment or NAV weights. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expenses` | `array` | Yes | List of expense objects, each with `description`, `amount`, and optionally `expense_type`. |
| `share_classes` | `array` | Yes | List of share class objects, each with `name`, `commitment` (total LP commitment), and `nav` (current NAV). |
| `method` | `string` | No | Allocation weighting method: `"commitment"` (default) or `"nav"`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "expense_allocation_engine",
  "arguments": {
    "expenses": [
      {"description": "Audit fee Q4 2025", "amount": 120000, "expense_type": "audit"},
      {"description": "Legal - fund formation", "amount": 85000, "expense_type": "legal"}
    ],
    "share_classes": [
      {"name": "Class A (institutional)", "commitment": 80000000, "nav": 72000000},
      {"name": "Class B (retail)", "commitment": 20000000, "nav": 18500000}
    ],
    "method": "commitment"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "expense_allocation_engine"`.
