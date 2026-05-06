---
skill: assembly_line_orchestrator
category: orchestration
description: Frames the Haiku→Sonnet→Opus workflow and estimates token spend.
tier: free
inputs: task_id, brief
---

# Assembly Line Orchestrator

## Description
Frames the Haiku→Sonnet→Opus workflow and estimates token spend.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_id` | `string` | Yes |  |
| `brief` | `string` | Yes |  |
| `estimated_tokens` | `object` | No | Estimated tokens per stage (haiku/sonnet/opus). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "assembly_line_orchestrator",
  "arguments": {
    "task_id": "<task_id>",
    "brief": "<brief>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "assembly_line_orchestrator"`.
