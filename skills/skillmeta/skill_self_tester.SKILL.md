---
skill: skill_self_tester
category: skillmeta
description: Generates test payloads from TOOL_META.inputSchema and runs the skill function.
tier: free
inputs: skill_module_path
---

# Skill Self Tester

## Description
Generates test payloads from TOOL_META.inputSchema and runs the skill function.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_module_path` | `string` | Yes |  |
| `num_tests` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_self_tester",
  "arguments": {
    "skill_module_path": "<skill_module_path>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_self_tester"`.
