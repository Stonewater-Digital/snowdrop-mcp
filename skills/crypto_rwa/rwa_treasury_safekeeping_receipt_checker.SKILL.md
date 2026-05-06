---
skill: rwa_treasury_safekeeping_receipt_checker
category: crypto_rwa
description: Validates safekeeping receipts and custodial chain-of-control for token wrappers.
tier: free
inputs: payload
---

# Rwa Treasury Safekeeping Receipt Checker

## Description
Validates safekeeping receipts and custodial chain-of-control for token wrappers.

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
  "tool": "rwa_treasury_safekeeping_receipt_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_safekeeping_receipt_checker"`.
