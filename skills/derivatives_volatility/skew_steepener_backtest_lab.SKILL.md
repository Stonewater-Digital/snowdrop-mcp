---
skill: skew_steepener_backtest_lab
category: derivatives_volatility
description: Backtests skew steepener ideas across time using synthetic option data.
tier: free
inputs: none
---

# Skew Steepener Backtest Lab

## Description
Backtests skew steepener ideas across time using synthetic option data.

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
  "tool": "skew_steepener_backtest_lab",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skew_steepener_backtest_lab"`.
