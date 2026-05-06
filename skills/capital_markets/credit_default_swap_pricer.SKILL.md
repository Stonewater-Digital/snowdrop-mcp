---
skill: credit_default_swap_pricer
category: capital_markets
description: Converts CDS spreads into implied default probabilities and expected losses.
tier: free
inputs: cds_spread_bps, recovery_rate, notional, maturity_years
---

# Credit Default Swap Pricer

## Description
Converts CDS spreads into implied default probabilities and expected losses. Derives annual and cumulative default probability, annual premium cash flows, and total expected loss for a single-name CDS position. Classifies credit quality as investment grade (IG) or high yield (HY).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cds_spread_bps` | `integer` | Yes | CDS spread in basis points (e.g. 150 for 150 bps). |
| `recovery_rate` | `number` | Yes | Assumed recovery rate as a decimal (e.g. 0.40 for 40%). |
| `notional` | `number` | Yes | Notional protection amount in dollars. |
| `maturity_years` | `integer` | Yes | Remaining maturity of the CDS contract in years. |
| `payment_frequency` | `string` | No | Payment frequency: "quarterly" (default: "quarterly"). |

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
    "cds_spread_bps": 150,
    "recovery_rate": 0.40,
    "notional": 10000000,
    "maturity_years": 5,
    "payment_frequency": "quarterly"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_default_swap_pricer"`.
