---
skill: tier2_instrument_amortization
category: regulatory_capital
description: Calculates remaining Tier 2 recognition after applying 20% annual haircuts during final 5 years.
tier: free
inputs: instrument_notional, original_maturity_years, remaining_maturity_years
---

# Tier2 Instrument Amortization

## Description
Calculates remaining Tier 2 recognition after applying 20% annual haircuts during final 5 years.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `instrument_notional` | `number` | Yes | Current nominal amount. |
| `original_maturity_years` | `number` | Yes | Original contractual maturity. |
| `remaining_maturity_years` | `number` | Yes | Years left until maturity. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tier2_instrument_amortization",
  "arguments": {
    "instrument_notional": 0,
    "original_maturity_years": 0,
    "remaining_maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tier2_instrument_amortization"`.
