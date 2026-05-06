---
skill: two_stage_ddm
category: market_analytics
description: Discounts dividends through a high-growth phase and a terminal perpetuity.
tier: free
inputs: current_dividend, high_growth_rate, high_growth_years, terminal_growth_rate, required_return
---

# Two Stage Ddm

## Description
Discounts dividends through a high-growth phase and a terminal perpetuity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_dividend` | `number` | Yes | Most recent dividend per share. |
| `high_growth_rate` | `number` | Yes | Growth rate during stage 1 (decimal). |
| `high_growth_years` | `integer` | Yes | Years of high growth. |
| `terminal_growth_rate` | `number` | Yes | Perpetual growth rate after stage 1. |
| `required_return` | `number` | Yes | Discount rate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "two_stage_ddm",
  "arguments": {
    "current_dividend": 0,
    "high_growth_rate": 0,
    "high_growth_years": 0,
    "terminal_growth_rate": 0,
    "required_return": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "two_stage_ddm"`.
