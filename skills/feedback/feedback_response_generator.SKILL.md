---
skill: feedback_response_generator
category: feedback
description: Generates human-like responses to agent feedback with priority flags.
tier: free
inputs: feedback
---

# Feedback Response Generator

## Description
Generates human-like responses to agent feedback with priority flags.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `feedback` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "feedback_response_generator",
  "arguments": {
    "feedback": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "feedback_response_generator"`.
