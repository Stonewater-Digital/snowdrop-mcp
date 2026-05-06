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
| `operation` | `string` | Yes |  |
| `account` | `['object', 'null']` | No |  |
| `query` | `['string', 'null']` | No | Search text |

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
