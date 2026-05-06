---
skill: skill_builder
category: root
description: Meta-skill: takes a plain-English skill description and generates a production-ready Snowdrop Python skill module via the Assembly Line (Haiku drafts, Sonnet polishes, Opus certifies for jury-tier complexity). Optionally writes the result to disk.
tier: free
inputs: name, purpose, inputs, outputs
---

# Skill Builder

## Description
Meta-skill: takes a plain-English skill description and generates a production-ready Snowdrop Python skill module via the Assembly Line (Haiku drafts, Sonnet polishes, Opus certifies for jury-tier complexity). Optionally writes the result to disk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | `string` | Yes | snake_case module name for the new skill (e.g. 'fetch_price'). |
| `purpose` | `string` | Yes | One sentence describing what the skill does. |
| `inputs` | `string` | Yes | Description of the skill's input parameters and their types. |
| `outputs` | `string` | Yes | Description of what the skill returns. |
| `complexity` | `string` | No | Assembly line tier. 'standard' uses Haiku + Sonnet. 'jury' adds Opus final review. |
| `write_to_disk` | `boolean` | No | If true, writes the generated code to skills/{name}.py. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_builder",
  "arguments": {
    "name": "<name>",
    "purpose": "<purpose>",
    "inputs": "<inputs>",
    "outputs": "<outputs>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_builder"`.
