---
skill: token_standard_travel_rule_payload_builder
category: crypto_rwa
description: Builds Travel Rule payloads for off-ramp transactions initiated by RWA tokens.
tier: free
inputs: payload
---

# Token Standard Travel Rule Payload Builder

## Description
Builds Travel Rule payloads for off-ramp transactions initiated by RWA tokens.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_standard_travel_rule_payload_builder",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_travel_rule_payload_builder"`.
