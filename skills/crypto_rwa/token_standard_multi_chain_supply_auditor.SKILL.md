---
skill: token_standard_multi_chain_supply_auditor
category: crypto_rwa
description: Audits circulating supply across chains to prevent double listings.
tier: free
inputs: payload
---

# Token Standard Multi Chain Supply Auditor

## Description
Audits circulating supply across chains to prevent double listings.

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
  "tool": "token_standard_multi_chain_supply_auditor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_multi_chain_supply_auditor"`.
