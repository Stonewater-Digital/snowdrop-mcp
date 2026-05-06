---
skill: rwa_real_estate_escrow_disbursement_chain_watcher
category: crypto_rwa
description: Traces escrow disbursements to ensure fiat releases mirror token allocation events.
tier: free
inputs: payload
---

# Rwa Real Estate Escrow Disbursement Chain Watcher

## Description
Traces escrow disbursements to ensure fiat releases mirror token allocation events.

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
  "tool": "rwa_real_estate_escrow_disbursement_chain_watcher",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_escrow_disbursement_chain_watcher"`.
