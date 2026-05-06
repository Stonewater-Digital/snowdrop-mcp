---
skill: feedback_collector
category: feedback
description: Stores categorized feedback with auto-responses.
tier: free
inputs: agent_id, feedback_type, message
---

# Feedback Collector

## Description
Stores categorized feedback with auto-responses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `feedback_type` | `string` | Yes |  |
| `skill_name` | `string` | No |  |
| `message` | `string` | Yes |  |
| `rating` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "feedback_collector",
  "arguments": {
    "agent_id": "<agent_id>",
    "feedback_type": "<feedback_type>",
    "message": "<message>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "feedback_collector"`.
