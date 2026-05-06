---
skill: skill_doc_generator
category: docs
description: Renders markdown docs for a skill module's TOOL_META.
tier: free
inputs: none
---

# Skill Doc Generator

## Description
Renders markdown docs for a skill module's TOOL_META.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_module_path` | `string` | No | Path to the Python module containing TOOL_META. |
| `tool_meta` | `object` | No | Optional TOOL_META dict provided directly. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_doc_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_doc_generator"`.
