---
skill: context_window_optimizer
category: memory
description: Packs content sections into the available context window using priority heuristics.
tier: free
inputs: content_sections, max_tokens
---

# Context Window Optimizer

## Description
Packs content sections into the available context window using priority heuristics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `content_sections` | `array` | Yes | Sections with name, content, priority (1-5) and estimated_tokens. |
| `max_tokens` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "context_window_optimizer",
  "arguments": {
    "content_sections": [],
    "max_tokens": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "context_window_optimizer"`.
