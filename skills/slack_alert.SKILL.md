---
skill: slack_alert
category: root
description: Send a message to Snowdrop's Slack channel. Used for real-time alerts to Thunder: price moves, audit results, integrity alerts, status updates.
tier: free
inputs: action
---

# Slack Alert

## Description
Send a message to Snowdrop's Slack channel. Used for real-time alerts to Thunder: price moves, audit results, integrity alerts, status updates. Actions: send (post message), ping (connectivity test).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation: 'send' to post a message, 'ping' for connectivity test. |
| `message` | `string` | No | Message text (plain text or Slack mrkdwn). Required for 'send'. |
| `channel_id` | `string` | No | Slack channel ID (falls back to SLACK_CHANNEL_ID env var). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "slack_alert",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "slack_alert"`.
