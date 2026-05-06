---
skill: collections_manager
category: credit
description: Tiers overdue accounts into reminder, notice, suspension, or write off stages.
tier: free
inputs: overdue_accounts
---

# Collections Manager

## Description
Tiers overdue accounts into reminder, notice, suspension, or write off stages.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `overdue_accounts` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "collections_manager",
  "arguments": {
    "overdue_accounts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "collections_manager"`.
