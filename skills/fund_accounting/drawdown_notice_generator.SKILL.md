---
skill: drawdown_notice_generator
category: fund_accounting
description: Produce structured LP drawdown notices and routing metadata. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_name, capital_call_pct, lp_commitments, call_date, notify_thunder
---

# Drawdown Notice Generator

## Description
Produce structured LP drawdown notices and routing metadata. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_name` | `string` | Yes | Legal name of the fund issuing the capital call. |
| `capital_call_pct` | `number` | Yes | Percentage of each LP's unfunded commitment being called (e.g. `0.25` for 25%). |
| `lp_commitments` | `array` | Yes | List of LP objects with `name`, `total_commitment`, and `amount_called_to_date` fields. |
| `call_date` | `string` | No | ISO 8601 date the notice is dated (defaults to today if omitted). |
| `notify_thunder` | `boolean` | No | If `true`, sends drawdown summary alert to Thunder. Defaults to `false`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "drawdown_notice_generator",
  "arguments": {
    "fund_name": "Snowdrop Opportunity Fund II, L.P.",
    "capital_call_pct": 0.20,
    "lp_commitments": [
      {"name": "State Pension Fund A", "total_commitment": 10000000, "amount_called_to_date": 4000000},
      {"name": "Endowment Capital LLC", "total_commitment": 5000000, "amount_called_to_date": 2000000}
    ],
    "call_date": "2026-06-15",
    "notify_thunder": false
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "drawdown_notice_generator"`.
