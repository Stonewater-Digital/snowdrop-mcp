---
skill: token_standard_redemption_notice_builder
category: crypto_rwa
description: Crafts redemption notice packets with deadlines and KYC refresh requests.
tier: free
inputs: payload
---

# Token Standard Redemption Notice Builder

## Description
Crafts redemption notice packets with deadlines and KYC refresh requests.

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
  "tool": "token_standard_redemption_notice_builder",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_redemption_notice_builder"`.
