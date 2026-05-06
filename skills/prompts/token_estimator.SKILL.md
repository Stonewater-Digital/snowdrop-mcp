---
skill: token_estimator
category: prompts
description: Estimates token counts and costs across Claude/GPT/Gemini families.
tier: free
inputs: text, model_family
---

# Token Estimator

## Description
Estimates token counts and costs across Claude/GPT/Gemini families.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | `string` | Yes |  |
| `model_family` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_estimator",
  "arguments": {
    "text": "<text>",
    "model_family": "<model_family>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_estimator"`.
