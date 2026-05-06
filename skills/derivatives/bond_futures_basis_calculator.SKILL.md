---
skill: bond_futures_basis_calculator
category: derivatives
description: Identifies CTD bond and computes gross/net basis for bond futures.
tier: free
inputs: bonds, futures_price, financing_rate_pct, days_to_delivery
---

# Bond Futures Basis Calculator

## Description
Identifies CTD bond and computes gross/net basis for bond futures.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bonds` | `array` | Yes | List of deliverable bonds. |
| `futures_price` | `number` | Yes | Current futures price (clean). Must be > 0. |
| `financing_rate_pct` | `number` | Yes | Repo / financing rate as a percentage (annual, actual/360). |
| `days_to_delivery` | `integer` | Yes | Days from today to futures delivery date. Must be >= 1. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bond_futures_basis_calculator",
  "arguments": {
    "bonds": [],
    "futures_price": 0,
    "financing_rate_pct": 0,
    "days_to_delivery": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_futures_basis_calculator"`.
