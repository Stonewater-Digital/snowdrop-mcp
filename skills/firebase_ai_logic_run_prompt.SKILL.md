---
skill: firebase_ai_logic_run_prompt
category: root
description: Execute a Firebase AI Logic prompt template with provided variables. Returns the model's text response.
tier: free
inputs: user_message
---

# Firebase Ai Logic Run Prompt

## Description
Execute a Firebase AI Logic prompt template with provided variables. Returns the model's text response.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_message` | `string` | Yes |  |
| `system_instruction` | `string` | No |  |
| `template_id` | `string` | No |  |
| `variables` | `object` | No |  |
| `project_id` | `string` | No |  |
| `location` | `string` | No |  |
| `model` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_ai_logic_run_prompt",
  "arguments": {
    "user_message": "<user_message>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_ai_logic_run_prompt"`.
