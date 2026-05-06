---
skill: openrouter_cost_logger
category: orchestration
description: Calculates OpenRouter call costs using the internal pricing table.
tier: free
inputs: model, input_tokens, output_tokens, purpose
---

# Openrouter Cost Logger

## Description
Calculates OpenRouter call costs using the internal pricing table.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `model` | `string` | Yes | Model slug (haiku/sonnet/opus). |
| `input_tokens` | `integer` | Yes |  |
| `output_tokens` | `integer` | Yes |  |
| `purpose` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "openrouter_cost_logger",
  "arguments": {
    "model": "<model>",
    "input_tokens": 0,
    "output_tokens": 0,
    "purpose": "<purpose>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "openrouter_cost_logger"`.
