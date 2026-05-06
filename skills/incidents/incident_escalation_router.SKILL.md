---
skill: incident_escalation_router
category: incidents
description: Determines escalation targets and automatic guardrails based on severity.
tier: free
inputs: incident
---

# Incident Escalation Router

## Description
Determines escalation targets and automatic guardrails based on severity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `incident` | `object` | Yes | Incident payload including severity, affected systems, and domain. |
| `escalation_policy` | `object` | No | Optional override for severity routing rules. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "incident_escalation_router",
  "arguments": {
    "incident": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "incident_escalation_router"`.
