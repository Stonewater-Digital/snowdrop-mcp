---
skill: post_reorg_equity_liquidity_planner
category: advanced_equities_spinoffs_restructuring
description: Forecasts float, turnover, and lockups for newly listed post-reorg equities.
tier: free
inputs: none
---

# Post Reorg Equity Liquidity Planner

## Description
Forecasts float, turnover, and lockups for newly listed post-reorg equities.

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
  "tool": "post_reorg_equity_liquidity_planner",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "post_reorg_equity_liquidity_planner"`.
