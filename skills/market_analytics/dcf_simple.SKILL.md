---
skill: dcf_simple
category: market_analytics
description: Discounts forecast free cash flows and a Gordon terminal value to estimate EV.
tier: free
inputs: free_cash_flows, terminal_growth_rate, wacc
---

# Dcf Simple

## Description
Discounts forecast free cash flows and a Gordon terminal value to estimate EV.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `free_cash_flows` | `array` | Yes | Projected annual FCFs. |
| `terminal_growth_rate` | `number` | Yes | Perpetual growth rate after explicit period. |
| `wacc` | `number` | Yes | Weighted average cost of capital. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dcf_simple",
  "arguments": {
    "free_cash_flows": [],
    "terminal_growth_rate": 0,
    "wacc": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dcf_simple"`.
