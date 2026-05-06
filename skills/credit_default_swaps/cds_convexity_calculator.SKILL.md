---
skill: cds_convexity_calculator
category: credit_default_swaps
description: Estimates convexity impact from nonlinear CDS spread moves.
tier: free
inputs: notional, pv01, spread_delta_bps
---

# Cds Convexity Calculator

## Description
Estimates convexity impact from nonlinear CDS spread moves.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `pv01` | `number` | Yes |  |
| `spread_delta_bps` | `number` | Yes |  |
| `spread_gamma` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_convexity_calculator",
  "arguments": {
    "notional": 0,
    "pv01": 0,
    "spread_delta_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_convexity_calculator"`.
