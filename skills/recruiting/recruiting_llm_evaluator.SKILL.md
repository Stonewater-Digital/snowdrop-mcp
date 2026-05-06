---
skill: recruiting_llm_evaluator
category: recruiting
description: System prompt for the evaluation task.
tier: free
inputs: prompt, context, task_tier, trace_id
---

# Recruiting Llm Evaluator

## Description
System prompt for the evaluation task.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prompt` | `string` | Yes |  |
| `context` | `string` | Yes |  |
| `task_tier` | `string` | Yes |  |
| `trace_id` | `string` | Yes |  |
| `response_format` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "recruiting_llm_evaluator",
  "arguments": {
    "prompt": "<prompt>",
    "context": "<context>",
    "task_tier": "<task_tier>",
    "trace_id": "<trace_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recruiting_llm_evaluator"`.
