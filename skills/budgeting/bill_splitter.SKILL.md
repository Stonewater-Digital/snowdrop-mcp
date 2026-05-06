---
skill: bill_splitter
category: budgeting
description: Splits a total bill amount evenly among a group of people, including tip calculation.
tier: free
inputs: total_amount, num_people
---

# Bill Splitter

## Description
Splits a total bill amount evenly among a group of people, including tip calculation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_amount` | `number` | Yes | Total bill amount before tip in dollars. |
| `num_people` | `integer` | Yes | Number of people splitting the bill. |
| `tip_pct` | `number` | No | Tip percentage (default: 18). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bill_splitter",
  "arguments": {
    "total_amount": 0,
    "num_people": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bill_splitter"`.
