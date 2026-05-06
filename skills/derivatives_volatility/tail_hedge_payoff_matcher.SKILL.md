---
skill: tail_hedge_payoff_matcher
category: derivatives_volatility
description: Matches portfolio beta to best-fit tail hedge structures with payoff tables.
tier: free
inputs: none
---

# Tail Hedge Payoff Matcher

## Description
Matches portfolio beta to best-fit tail hedge structures with payoff tables.

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
  "tool": "tail_hedge_payoff_matcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tail_hedge_payoff_matcher"`.
