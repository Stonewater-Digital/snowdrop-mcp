---
skill: rate_limit_cascade
category: orchestration
description: Downgrades Opus→Sonnet→Haiku→Grok when a model is saturated.
tier: free
inputs: requested_model, rate_limit_state
---

# Rate Limit Cascade

## Description
Downgrades Opus→Sonnet→Haiku→Grok when a model is saturated.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `requested_model` | `string` | Yes |  |
| `rate_limit_state` | `object` | Yes | Remaining invocation counts per model. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rate_limit_cascade",
  "arguments": {
    "requested_model": "<requested_model>",
    "rate_limit_state": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rate_limit_cascade"`.
