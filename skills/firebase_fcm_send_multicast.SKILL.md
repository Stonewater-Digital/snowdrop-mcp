---
skill: firebase_fcm_send_multicast
category: root
description: Send FCM push notification to up to 500 device tokens simultaneously. Returns success_count, failure_count, and per-token results.
tier: free
inputs: tokens, title, body
---

# Firebase Fcm Send Multicast

## Description
Send FCM push notification to up to 500 device tokens simultaneously. Returns success_count, failure_count, and per-token results.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tokens` | `any` | Yes |  |
| `title` | `string` | Yes |  |
| `body` | `string` | Yes |  |
| `data` | `object` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_fcm_send_multicast",
  "arguments": {
    "tokens": "<tokens>",
    "title": "<title>",
    "body": "<body>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_fcm_send_multicast"`.
