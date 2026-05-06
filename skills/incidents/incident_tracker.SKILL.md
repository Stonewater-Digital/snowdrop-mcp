---
skill: incident_tracker
category: incidents
description: Opens, updates, or lists incidents with SLA tracking and JSONL logging.
tier: free
inputs: operation
---

# Incident Tracker

## Description
Opens, updates, or lists incidents with SLA tracking and JSONL logging.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes | Operation to perform on the incident ledger. |
| `incident` | `object` | No | Incident payload for open/update operations. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "incident_tracker",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "incident_tracker"`.
