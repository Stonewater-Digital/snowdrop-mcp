---
skill: skill_dispatcher
category: nlp
description: Maps classified intents and extracted entities into MCP skill payloads.
tier: free
inputs: intent, entities, skill_registry
---

# Skill Dispatcher

## Description
Maps classified intents and extracted entities into MCP skill payloads.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `intent` | `string` | Yes |  |
| `entities` | `array` | Yes |  |
| `skill_registry` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_dispatcher",
  "arguments": {
    "intent": "<intent>",
    "entities": [],
    "skill_registry": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_dispatcher"`.
