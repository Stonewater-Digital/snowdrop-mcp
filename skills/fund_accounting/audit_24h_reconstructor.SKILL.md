---
skill: audit_24h_reconstructor
category: fund_accounting
description: Filters ledger activity to a 24h window and produces a running balance. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: target_date, transactions, opening_balance
---

# Audit 24h Reconstructor

## Description
Filters ledger activity to a 24h window and produces a running balance. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_date` | `string` | Yes | ISO 8601 date string (e.g. `"2025-12-31"`) for the 24-hour window to reconstruct. |
| `transactions` | `array` | Yes | List of ledger transaction objects, each with at minimum `date`, `amount`, and `description` fields. |
| `opening_balance` | `number` | No | Opening balance in base currency at the start of `target_date`. Defaults to `0.0`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "audit_24h_reconstructor",
  "arguments": {
    "target_date": "2025-12-31",
    "transactions": [
      {"date": "2025-12-31T09:15:00Z", "amount": 250000.00, "description": "Capital call receipt LP-07"},
      {"date": "2025-12-31T14:30:00Z", "amount": -75000.00, "description": "Management fee disbursement"}
    ],
    "opening_balance": 1500000.00
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "audit_24h_reconstructor"`.
