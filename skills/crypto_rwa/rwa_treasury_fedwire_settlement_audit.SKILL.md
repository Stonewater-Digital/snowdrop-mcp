---
skill: rwa_treasury_fedwire_settlement_audit
category: crypto_rwa
description: Maps Fedwire settlement receipts to blockchain proofs for custody assurance.
tier: free
inputs: payload
---

# Rwa Treasury Fedwire Settlement Audit

## Description
Maps Fedwire settlement receipts to blockchain proofs for custody assurance.

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
  "tool": "rwa_treasury_fedwire_settlement_audit",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_fedwire_settlement_audit"`.
