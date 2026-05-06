---
skill: recovery_runbook_generator
category: disaster_recovery
description: Outputs a step-by-step recovery plan tailored to the failure type.
tier: free
inputs: failure_type, available_backups, system_state
---

# Recovery Runbook Generator

## Description
Outputs a step-by-step recovery plan tailored to the failure type.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `failure_type` | `string` | Yes |  |
| `available_backups` | `array` | Yes |  |
| `system_state` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "recovery_runbook_generator",
  "arguments": {
    "failure_type": "<failure_type>",
    "available_backups": [],
    "system_state": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recovery_runbook_generator"`.
