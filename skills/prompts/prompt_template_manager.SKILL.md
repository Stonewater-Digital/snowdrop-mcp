---
skill: prompt_template_manager
category: prompts
description: Provides CRUD operations on config/prompt_templates.json.
tier: free
inputs: operation
---

# Prompt Template Manager

## Description
Provides CRUD operations on config/prompt_templates.json.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `template_name` | `string` | No |  |
| `template` | `['object', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "prompt_template_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "prompt_template_manager"`.
