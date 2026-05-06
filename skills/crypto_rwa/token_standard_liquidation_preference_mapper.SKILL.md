---
skill: token_standard_liquidation_preference_mapper
category: crypto_rwa
description: Maps liquidation preference stacks to ensure payouts follow documentation.
tier: free
inputs: payload
---

# Token Standard Liquidation Preference Mapper

## Description
Maps liquidation preference stacks to ensure payouts follow documentation.

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
  "tool": "token_standard_liquidation_preference_mapper",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_liquidation_preference_mapper"`.
