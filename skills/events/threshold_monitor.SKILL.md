---
skill: threshold_monitor
category: events
description: Evaluates metrics against warning and critical thresholds.
tier: free
inputs: metrics
---

# Threshold Monitor

## Description
Evaluates metrics against warning and critical thresholds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `metrics` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "threshold_monitor",
  "arguments": {
    "metrics": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "threshold_monitor"`.
