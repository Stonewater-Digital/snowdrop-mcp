---
skill: recruiting_llm_evaluator
category: recruiting
description: System prompt for the evaluation task.
tier: free
inputs: none
---

# Recruiting Llm Evaluator

## Description
System prompt for the evaluation task.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "recruiting_llm_evaluator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recruiting_llm_evaluator"`.
