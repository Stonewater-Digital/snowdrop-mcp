---
skill: firebase_fcm_send
category: root
description: Send a single FCM push notification to a device registration token, topic, or condition. Returns message_id on success.
tier: free
inputs: none
---

# Firebase Fcm Send

## Description
Send a single FCM push notification to a device registration token, topic, or condition. Returns message_id on success.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_fcm_send",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_fcm_send"`.
