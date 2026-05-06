---
skill: skill_dependency_mapper
category: skillmeta
description: Scans skill files for env vars, internal imports, and external API references.
tier: free
inputs: none
---

# Skill Dependency Mapper

## Description
Scans skill files for env vars, internal imports, and external API references.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_directory` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_dependency_mapper",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_dependency_mapper"`.
