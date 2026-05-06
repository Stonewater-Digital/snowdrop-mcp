---
skill: telegram_command_router
category: telegram_skills
description: Parses Telegram commands (/balance, /audit, /brief, /price, /status, /help).
tier: free
inputs: command_text, chat_id
---

# Telegram Command Router

## Description
Parses Telegram commands (/balance, /audit, /brief, /price, /status, /help).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `command_text` | `string` | Yes |  |
| `chat_id` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "telegram_command_router",
  "arguments": {
    "command_text": "<command_text>",
    "chat_id": "<chat_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "telegram_command_router"`.
