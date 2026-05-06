---
skill: token_standard_secondary_liquidity_gater
category: crypto_rwa
description: Controls secondary trading windows based on issuer-defined liquidity tiers.
tier: free
inputs: payload
---

# Token Standard Secondary Liquidity Gater

## Description
Controls secondary trading windows based on issuer-defined liquidity tiers.

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
  "tool": "token_standard_secondary_liquidity_gater",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_secondary_liquidity_gater"`.
