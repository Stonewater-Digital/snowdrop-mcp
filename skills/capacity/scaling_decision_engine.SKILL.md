---
skill: scaling_decision_engine
category: capacity
description: Evaluates telemetry against thresholds to suggest scale up/down/hold.
tier: free
inputs: current_metrics, thresholds
---

# Scaling Decision Engine

## Description
Evaluates telemetry against thresholds to suggest scale up/down/hold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_metrics` | `object` | Yes |  |
| `thresholds` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "scaling_decision_engine",
  "arguments": {
    "current_metrics": {},
    "thresholds": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "scaling_decision_engine"`.
