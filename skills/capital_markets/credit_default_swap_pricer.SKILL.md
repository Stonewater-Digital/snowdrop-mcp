---
skill: credit_default_swap_pricer
category: capital_markets
description: Converts CDS spreads into implied default probabilities and expected losses.
tier: free
inputs: cds_spread_bps, recovery_rate, notional, maturity_years
---

# Credit Default Swap Pricer

## Description
Converts CDS spreads into implied default probabilities and expected losses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cds_spread_bps` | `integer` | Yes |  |
| `recovery_rate` | `number` | Yes |  |
| `notional` | `number` | Yes |  |
| `maturity_years` | `integer` | Yes |  |
| `payment_frequency` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_default_swap_pricer",
  "arguments": {
    "cds_spread_bps": 0,
    "recovery_rate": 0,
    "notional": 0,
    "maturity_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_default_swap_pricer"`.
