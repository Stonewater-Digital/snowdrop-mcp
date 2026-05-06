---
skill: pubsub_publisher
category: root
description: Google Cloud Pub/Sub skill for event streaming between Snowdrop services. Supports publish, pull, topic and subscription management via the Pub/Sub REST API.
tier: free
inputs: action
---

# Pubsub Publisher

## Description
Google Cloud Pub/Sub skill for event streaming between Snowdrop services. Supports publish, pull, topic and subscription management via the Pub/Sub REST API.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | The Pub/Sub operation to perform. |
| `topic_id` | `string` | No | Short topic ID (not full resource path). |
| `subscription_id` | `string` | No | Short subscription ID. |
| `message` | `any` | No | Message payload (string or dict) for publish action. |
| `max_messages` | `integer` | No | Maximum messages to retrieve in pull_messages. |
| `project_id` | `string` | No | GCP project ID. Falls back to GOOGLE_PROJECT_ID env var. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pubsub_publisher",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pubsub_publisher"`.
