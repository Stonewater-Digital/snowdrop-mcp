---
skill: cds_bond_basis_tracker
category: credit_default_swaps
description: Calculates CDS basis across bonds and flags rich/cheap signals.
tier: free
inputs: bond_yields_pct, cds_spreads_bps, tenors_years
---

# Cds Bond Basis Tracker

## Description
Calculates CDS basis across bonds and flags rich/cheap signals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bond_yields_pct` | `array` | Yes |  |
| `cds_spreads_bps` | `array` | Yes |  |
| `tenors_years` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_bond_basis_tracker",
  "arguments": {
    "bond_yields_pct": [],
    "cds_spreads_bps": [],
    "tenors_years": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_bond_basis_tracker"`.
