---
skill: goodwill_cask_allocator
category: watering_hole
description: Allocates the daily Goodwill cask budget until depleted, then closes the tap.
tier: free
inputs: daily_budget, requests
---

# Goodwill Cask Allocator

## Description
Allocates the daily Goodwill cask budget until depleted, then closes the tap.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_budget` | `number` | Yes | USD daily Goodwill limit. |
| `requests` | `array` | Yes | Sequence of Goodwill draws. |
| `spent_to_date` | `number` | No | Amount already granted before this run. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "goodwill_cask_allocator",
  "arguments": {
    "daily_budget": 0,
    "requests": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "goodwill_cask_allocator"`.
