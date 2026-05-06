---
skill: price_alert_evaluator
category: events
description: Checks price conditions (above, below, pct_change) and prioritizes alerts.
tier: free
inputs: alerts
---

# Price Alert Evaluator

## Description
Checks price conditions (above, below, pct_change) and prioritizes alerts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `alerts` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "price_alert_evaluator",
  "arguments": {
    "alerts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "price_alert_evaluator"`.
