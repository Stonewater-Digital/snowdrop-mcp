---
skill: api_playground_provider
category: playground
description: Generates sample inputs and sandboxed outputs for public skill demos.
tier: free
inputs: skill_name
---

# Api Playground Provider

## Description
Generates sample inputs and sandboxed outputs for public skill demos.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_name` | `string` | Yes |  |
| `custom_input` | `['object', 'null']` | No |  |
| `use_sample` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "api_playground_provider",
  "arguments": {
    "skill_name": "<skill_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_playground_provider"`.
