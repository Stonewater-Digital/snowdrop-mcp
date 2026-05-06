---
skill: chart_of_accounts
category: accounting
description: Adds or searches accounts across the Stonewater standard chart.
tier: free
inputs: operation
---

# Chart Of Accounts

## Description
Adds or searches accounts across the Stonewater standard chart.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes | Action to perform: `"add"` to create a new account, `"search"` to find existing accounts. |
| `account` | `object` | No | Account payload for `add` operations; requires `account_number`, `name`, and `type` (asset/liability/equity/revenue/expense). |
| `query` | `string` | No | Search text matched against account number, name, or type for `search` operations. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "chart_of_accounts",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chart_of_accounts"`.
