---
skill: central_bank_ledger_sync
category: sovereign
description: Reconciles a CBDC transaction ledger against central bank balance and reported circulation figures to detect discrepancies.
tier: free
inputs: cbdc_ledger, central_bank_balance, reported_circulation
---

# Central Bank Ledger Sync

## Description
Reconciles a CBDC transaction ledger against central bank balance and reported circulation figures to detect discrepancies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cbdc_ledger` | `array` | Yes | List of CBDC transactions |
| `central_bank_balance` | `number` | Yes | Authoritative balance at central bank in currency units |
| `reported_circulation` | `number` | Yes | Official reported CBDC in circulation |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "central_bank_ledger_sync",
  "arguments": {
    "cbdc_ledger": [],
    "central_bank_balance": 0,
    "reported_circulation": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "central_bank_ledger_sync"`.
