---
skill: webhook_receiver
category: integrations
description: Verifies webhook signatures and normalizes payloads.
tier: free
inputs: source, headers, payload
---

# Webhook Receiver

## Description
Verifies webhook signatures and normalizes payloads.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `source` | `string` | Yes |  |
| `headers` | `object` | Yes |  |
| `payload` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "webhook_receiver",
  "arguments": {
    "source": "<source>",
    "headers": {},
    "payload": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "webhook_receiver"`.
