---
skill: administrator_api_bridge
category: data_ingestion
description: Bridge skill that validates administrator feeds and emits normalized payload summaries.
tier: free
inputs: responses, required_fields
---

# Administrator Api Bridge

## Description
Bridge skill that validates administrator feeds and emits normalized payload summaries.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `responses` | `array` | Yes | Admin payloads with keys: source, endpoint, received_at, records[]. |
| `required_fields` | `array` | Yes | Fields that must exist in each record for downstream posting. |
| `max_age_minutes` | `integer` | No | Maximum acceptable payload age before marking as stale. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "administrator_api_bridge",
  "arguments": {
    "responses": [],
    "required_fields": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "administrator_api_bridge"`.
