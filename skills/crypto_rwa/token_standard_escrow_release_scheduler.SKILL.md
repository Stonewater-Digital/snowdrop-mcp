---
skill: token_standard_escrow_release_scheduler
category: crypto_rwa
description: Schedules escrow release events based on oracle-verified milestones.
tier: free
inputs: payload
---

# Token Standard Escrow Release Scheduler

## Description
Schedules escrow release events based on oracle-verified milestones.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_standard_escrow_release_scheduler",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_escrow_release_scheduler"`.
