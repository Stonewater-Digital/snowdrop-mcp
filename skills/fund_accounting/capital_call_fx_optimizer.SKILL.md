---
skill: capital_call_fx_optimizer
category: fund_accounting
description: Allocates multi-currency balances to satisfy a capital call with minimal FX drag. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_currency, capital_call_amount, currency_positions, notify_thunder
---

# Capital Call Fx Optimizer

## Description
Allocates multi-currency balances to satisfy a capital call with minimal FX drag. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_currency` | `string` | Yes | Base currency of the fund (e.g. `"USD"`). |
| `capital_call_amount` | `number` | Yes | Total capital call amount in the fund's base currency. |
| `currency_positions` | `array` | Yes | List of currency position objects, each with `currency`, `balance`, and `fx_rate` (rate to fund currency). |
| `notify_thunder` | `boolean` | No | If `true`, sends an alert to Thunder when FX drag exceeds threshold. Defaults to `false`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_call_fx_optimizer",
  "arguments": {
    "fund_currency": "USD",
    "capital_call_amount": 2500000,
    "currency_positions": [
      {"currency": "USD", "balance": 1800000, "fx_rate": 1.0},
      {"currency": "EUR", "balance": 900000, "fx_rate": 1.08},
      {"currency": "GBP", "balance": 400000, "fx_rate": 1.27}
    ],
    "notify_thunder": false
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_call_fx_optimizer"`.
