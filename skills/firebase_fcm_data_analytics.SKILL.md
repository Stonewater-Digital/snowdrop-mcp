---
skill: firebase_fcm_data_analytics
category: root
description: Get Firebase Cloud Messaging delivery analytics data — send counts, delivery rates, and open rates for a date range.
tier: free
inputs: none
---

# Firebase Fcm Data Analytics

## Description
Get Firebase Cloud Messaging delivery analytics data — send counts, delivery rates, and open rates for a date range.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project_id` | `string` | No |  |
| `start_date` | `string` | No |  |
| `end_date` | `string` | No |  |
| `app_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_fcm_data_analytics",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_fcm_data_analytics"`.
