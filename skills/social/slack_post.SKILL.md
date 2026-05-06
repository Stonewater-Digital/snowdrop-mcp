---
skill: slack_post
category: social
description: Post a message to the Snowdrop Slack channel. Used for daily engagement reports, milestone alerts, and status updates to Thunder.
tier: free
inputs: message
---

# Slack Post

## Description
Post a message to the Snowdrop Slack channel. Used for daily engagement reports, milestone alerts, and status updates to Thunder. Requires SLACK_BOT_TOKEN and SLACK_CHANNEL_ID environment variables.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `string` | Yes |  |
| `channel_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "slack_post",
  "arguments": {
    "message": "<message>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "slack_post"`.
