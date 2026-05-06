---
skill: implied_vs_realized_carry_calculator
category: derivatives_volatility
description: Compares implied carry vs. realized vol for vol selling strategies.
tier: free
inputs: none
---

# Implied Vs Realized Carry Calculator

## Description
Compares implied carry vs. realized vol for vol selling strategies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tickers` | `array` | No | Tickers or identifiers relevant to the analysis focus. |
| `lookback_days` | `integer` | No | Historical window (days) for synthetic / free-data calculations. |
| `analysis_notes` | `string` | No | Optional qualitative context to embed in the response. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "implied_vs_realized_carry_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "implied_vs_realized_carry_calculator"`.
