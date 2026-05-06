---
skill: wash_sale_rule_checker
category: securities_tax
description: Checks transaction logs for wash sales inside 30-day windows.
tier: free
inputs: transactions
---

# Wash Sale Rule Checker

## Description
Checks transaction logs for wash sales inside 30-day windows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transactions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "wash_sale_rule_checker",
  "arguments": {
    "transactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "wash_sale_rule_checker"`.
