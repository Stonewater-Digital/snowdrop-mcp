---
skill: smart_contract_vault_share_dilution_checker
category: crypto_rwa
description: Models share issuance math to catch dilution vectors for vault depositors.
tier: free
inputs: payload
---

# Smart Contract Vault Share Dilution Checker

## Description
Models share issuance math to catch dilution vectors for vault depositors.

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
  "tool": "smart_contract_vault_share_dilution_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_vault_share_dilution_checker"`.
