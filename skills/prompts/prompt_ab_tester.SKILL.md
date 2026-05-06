---
skill: prompt_ab_tester
category: prompts
description: Appends prompt experiment outcomes and computes per-variant stats.
tier: free
inputs: test_name, variant, result
---

# Prompt Ab Tester

## Description
Appends prompt experiment outcomes and computes per-variant stats.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `test_name` | `string` | Yes |  |
| `variant` | `string` | Yes |  |
| `result` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "prompt_ab_tester",
  "arguments": {
    "test_name": "<test_name>",
    "variant": "<variant>",
    "result": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "prompt_ab_tester"`.
