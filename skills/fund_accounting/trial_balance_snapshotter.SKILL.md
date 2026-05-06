---
skill: trial_balance_snapshotter
category: fund_accounting
description: Converts ledger entries into a base-currency trial balance and highlights NAV deltas. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: ledger_entries, base_currency, fx_rates
---

# Trial Balance Snapshotter

## Description
Converts ledger entries into a base-currency trial balance and highlights NAV deltas. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ledger_entries` | `array` | Yes | List of ledger entry objects, each with `account`, `debit`, `credit`, `currency`, and `date`. |
| `base_currency` | `string` | No | Base currency for the trial balance (e.g. `"USD"`). Defaults to `"USD"`. |
| `fx_rates` | `object` | No | Map of currency codes to USD conversion rates (e.g. `{"EUR": 1.08, "GBP": 1.27}`). Required if entries contain non-base currencies. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trial_balance_snapshotter",
  "arguments": {
    "ledger_entries": [
      {"account": "Cash - Mercury", "debit": 250000, "credit": 0, "currency": "USD", "date": "2026-03-31"},
      {"account": "LP Capital Called", "debit": 0, "credit": 250000, "currency": "USD", "date": "2026-03-31"},
      {"account": "Portfolio Investment - Fund I", "debit": 85000, "credit": 0, "currency": "EUR", "date": "2026-03-31"},
      {"account": "Accounts Payable - Mgmt Fee", "debit": 0, "credit": 85000, "currency": "EUR", "date": "2026-03-31"}
    ],
    "base_currency": "USD",
    "fx_rates": {"EUR": 1.08, "GBP": 1.27}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trial_balance_snapshotter"`.
