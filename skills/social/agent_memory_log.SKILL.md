---
skill: agent_memory_log
category: social
description: Log and retrieve memory about agents, developers, and community members Snowdrop has interacted with. Tracks: platforms where interaction occurred, topics discussed, star trades completed, job interest signals, follow-up actions needed, and sentiment.
tier: free
inputs: action
---

# Agent Memory Log

## Description
Log and retrieve memory about agents, developers, and community members Snowdrop has interacted with. Tracks: platforms where interaction occurred, topics discussed, star trades completed, job interest signals, follow-up actions needed, and sentiment. Uses Firestore for persistence. This is Snowdrop's CRM — she never forgets who she's met or what was said.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes |  |
| `agent_id` | `string` | No |  |
| `platform` | `string` | No |  |
| `note` | `string` | No |  |
| `tags` | `array` | No |  |
| `star_traded` | `boolean` | No |  |
| `follow_up` | `string` | No |  |
| `sentiment` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_memory_log",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_memory_log"`.
