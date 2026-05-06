---
skill: smart_contract_infinite_mint_sentinel
category: crypto_rwa
description: Detects code paths capable of unlimited minting without supply caps.
tier: free
inputs: payload
---

# Smart Contract Infinite Mint Sentinel

## Description
Detects code paths capable of unlimited minting without supply caps.

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
  "tool": "smart_contract_infinite_mint_sentinel",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_infinite_mint_sentinel"`.
