---
skill: reverse_dcf
category: market_analytics
description: Derives the growth rate required to justify the current market capitalization.
tier: free
inputs: market_cap, current_fcf, wacc, terminal_growth
---

# Reverse Dcf

## Description
Derives the growth rate required to justify the current market capitalization.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `market_cap` | `number` | Yes | Current enterprise/market value. |
| `current_fcf` | `number` | Yes | Last-twelve-month free cash flow. |
| `wacc` | `number` | Yes | Discount rate. |
| `terminal_growth` | `number` | Yes | Perpetual growth used in terminal value. |
| `projection_years` | `integer` | No | Years of explicit growth (default 5). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reverse_dcf",
  "arguments": {
    "market_cap": 0,
    "current_fcf": 0,
    "wacc": 0,
    "terminal_growth": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reverse_dcf"`.
