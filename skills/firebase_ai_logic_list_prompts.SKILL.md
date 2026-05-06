---
skill: firebase_ai_logic_list_prompts
category: root
description: List Firebase AI Logic server-side prompt templates for a project. Returns template IDs, model configurations, and system instructions.
tier: free
inputs: none
---

# Firebase Ai Logic List Prompts

## Description
List Firebase AI Logic server-side prompt templates for a project. Returns template IDs, model configurations, and system instructions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project_id` | `string` | No |  |
| `location` | `string` | No |  |
| `page_size` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_ai_logic_list_prompts",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_ai_logic_list_prompts"`.
