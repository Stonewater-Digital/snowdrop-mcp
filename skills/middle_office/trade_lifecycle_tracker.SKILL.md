---
skill: trade_lifecycle_tracker
category: middle_office
description: Summarizes trade lifecycle stages with elapsed times and bottlenecks.
tier: free
inputs: trades
---

# Trade Lifecycle Tracker

## Description
Summarizes trade lifecycle stages with elapsed times and bottlenecks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trades` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trade_lifecycle_tracker",
  "arguments": {
    "trades": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trade_lifecycle_tracker"`.
