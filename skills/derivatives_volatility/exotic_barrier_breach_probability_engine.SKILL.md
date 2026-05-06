---
skill: exotic_barrier_breach_probability_engine
category: derivatives_volatility
description: Estimates barrier hit probabilities using free implied vol data.
tier: free
inputs: none
---

# Exotic Barrier Breach Probability Engine

## Description
Estimates barrier hit probabilities using free implied vol data.

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
  "tool": "exotic_barrier_breach_probability_engine",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exotic_barrier_breach_probability_engine"`.
