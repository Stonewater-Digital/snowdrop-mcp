---
skill: email_alert_builder
category: notifications
description: Prepares email payloads without sending them.
tier: free
inputs: recipient, subject, body_sections
---

# Email Alert Builder

## Description
Prepares email payloads without sending them.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `recipient` | `string` | Yes |  |
| `subject` | `string` | Yes |  |
| `body_sections` | `array` | Yes |  |
| `priority` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "email_alert_builder",
  "arguments": {
    "recipient": "<recipient>",
    "subject": "<subject>",
    "body_sections": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "email_alert_builder"`.
