---
skill: savings_account_comparator
category: banking
description: Compare earnings across multiple savings accounts for a given principal over 1, 3, and 5 year horizons, ranked by returns.
tier: free
inputs: principal, accounts
---

# Savings Account Comparator

## Description
Compare earnings across multiple savings accounts for a given principal over 1, 3, and 5 year horizons, ranked by returns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Initial deposit amount. |
| `accounts` | `array` | Yes | List of savings accounts to compare. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "savings_account_comparator",
  "arguments": {
    "principal": 0,
    "accounts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "savings_account_comparator"`.
