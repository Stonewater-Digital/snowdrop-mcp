---
skill: jury_deliberation_orchestrator
category: jury
description: Structures prompts and verdicts for the Sonnet/Grok/Gemini debate loop.
tier: free
inputs: thesis
---

# Jury Deliberation Orchestrator

## Description
Structures prompts and verdicts for the Sonnet/Grok/Gemini debate loop.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `thesis` | `object` | Yes | Structured thesis payload (summary, confidence, risks, etc.). |
| `models` | `array` | No | Ordered model roster to involve in deliberation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "jury_deliberation_orchestrator",
  "arguments": {
    "thesis": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "jury_deliberation_orchestrator"`.
