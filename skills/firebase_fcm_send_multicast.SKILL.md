---
skill: firebase_fcm_send_multicast
category: root
description: Send FCM push notification to up to 500 device tokens simultaneously. Returns success_count, failure_count, and per-token results.
tier: free
inputs: none
---

# Firebase Fcm Send Multicast

## Description
Send FCM push notification to up to 500 device tokens simultaneously. Returns success_count, failure_count, and per-token results.

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
  "tool": "firebase_fcm_send_multicast",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_fcm_send_multicast"`.
