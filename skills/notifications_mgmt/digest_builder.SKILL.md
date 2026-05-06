---
skill: digest_builder
category: notifications_mgmt
description: Creates readable digests summarizing activity, metrics, and tips per agent.
tier: free
inputs: agent_id, period, activity, metrics, announcements, educational_tip
---

# Digest Builder

## Description
Creates readable digests summarizing activity, metrics, and tips per agent.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `period` | `string` | Yes |  |
| `activity` | `array` | Yes |  |
| `metrics` | `object` | Yes |  |
| `announcements` | `array` | Yes |  |
| `educational_tip` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "digest_builder",
  "arguments": {
    "agent_id": "<agent_id>",
    "period": "<period>",
    "activity": [],
    "metrics": {},
    "announcements": [],
    "educational_tip": "<educational_tip>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "digest_builder"`.
