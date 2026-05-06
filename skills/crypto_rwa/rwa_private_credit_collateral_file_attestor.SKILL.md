---
skill: rwa_private_credit_collateral_file_attestor
category: crypto_rwa
description: Confirms collateral file hashes and borrowing base calculations for on-chain lenders.
tier: free
inputs: payload
---

# Rwa Private Credit Collateral File Attestor

## Description
Confirms collateral file hashes and borrowing base calculations for on-chain lenders.

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
  "tool": "rwa_private_credit_collateral_file_attestor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_private_credit_collateral_file_attestor"`.
