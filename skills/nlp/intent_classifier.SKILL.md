---
skill: intent_classifier
category: nlp
description: Heuristically classifies operator text into MCP skill intents
tier: free
inputs: user_input, available_categories
---

# Intent Classifier

## Description
Heuristically classifies operator text into MCP skill intents

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_input` | `string` | Yes |  |
| `available_categories` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "intent_classifier",
  "arguments": {
    "user_input": "<user_input>",
    "available_categories": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intent_classifier"`.
