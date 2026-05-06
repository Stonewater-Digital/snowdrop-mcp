---
skill: recovery_rate_estimator
category: private_credit
description: Aggregates LGD and recovery percentages by class.
tier: free
inputs: positions
---

# Recovery Rate Estimator

## Description
Aggregates LGD and recovery percentages by class.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "recovery_rate_estimator",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recovery_rate_estimator"`.
