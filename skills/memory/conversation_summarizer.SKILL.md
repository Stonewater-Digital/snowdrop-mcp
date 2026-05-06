---
skill: conversation_summarizer
category: memory
description: Compress multi-turn logs into actionable decisions and questions.
tier: free
inputs: messages
---

# Conversation Summarizer

## Description
Compress multi-turn logs into actionable decisions and questions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `messages` | `array` | Yes | Chat messages containing role, content, timestamp. |
| `max_output_tokens` | `integer` | No | Maximum tokens to allocate for summary payload. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "conversation_summarizer",
  "arguments": {
    "messages": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "conversation_summarizer"`.
