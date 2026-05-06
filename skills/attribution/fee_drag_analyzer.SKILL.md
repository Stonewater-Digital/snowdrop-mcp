---
skill: fee_drag_analyzer
category: attribution
description: Summarizes fees and calculates annualized drag versus AUM.
tier: free
inputs: fees, avg_aum, period_days
---

# Fee Drag Analyzer

## Description
Summarizes fees and calculates annualized drag versus AUM.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fees` | `array` | Yes |  |
| `avg_aum` | `number` | Yes |  |
| `period_days` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fee_drag_analyzer",
  "arguments": {
    "fees": [],
    "avg_aum": 0,
    "period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fee_drag_analyzer"`.
