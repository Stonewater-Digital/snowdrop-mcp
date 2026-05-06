---
skill: deployment_readiness_checker
category: readiness
description: Aggregates deployment checklist results and surfaces blockers/warnings.
tier: free
inputs: checks
---

# Deployment Readiness Checker

## Description
Aggregates deployment checklist results and surfaces blockers/warnings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `checks` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "deployment_readiness_checker",
  "arguments": {
    "checks": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "deployment_readiness_checker"`.
