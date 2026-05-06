---
skill: special_dividend_arbitrage_planner
category: event_driven_trades
description: Evaluates pre/post special dividend payout value capture tactics including deep ITM options.
tier: free
inputs: none
---

# Special Dividend Arbitrage Planner

## Description
Evaluates pre/post special dividend payout value capture tactics including deep ITM options.

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
  "tool": "special_dividend_arbitrage_planner",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "special_dividend_arbitrage_planner"`.
