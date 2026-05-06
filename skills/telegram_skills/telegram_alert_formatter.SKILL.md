---
skill: telegram_alert_formatter
category: telegram_skills
description: Formats alerts using Telegram MarkdownV2 with escaping and CTA support.
tier: free
inputs: title, body_lines
---

# Telegram Alert Formatter

## Description
Formats alerts using Telegram MarkdownV2 with escaping and CTA support.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | `string` | Yes |  |
| `body_lines` | `array` | Yes |  |
| `cta_url` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "telegram_alert_formatter",
  "arguments": {
    "title": "<title>",
    "body_lines": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "telegram_alert_formatter"`.
