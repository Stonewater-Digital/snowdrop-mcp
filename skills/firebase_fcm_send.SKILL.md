---
skill: firebase_fcm_send
category: root
description: Send a single FCM push notification to a device registration token, topic, or condition. Returns message_id on success.
tier: free
inputs: title, body
---

# Firebase Fcm Send

## Description
Send a single FCM push notification to a device registration token, topic, or condition. Returns message_id on success.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | `string` | Yes |  |
| `body` | `string` | Yes |  |
| `token` | `string` | No |  |
| `topic` | `string` | No |  |
| `condition` | `string` | No |  |
| `data` | `object` | No |  |
| `image_url` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_fcm_send",
  "arguments": {
    "title": "<title>",
    "body": "<body>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_fcm_send"`.
