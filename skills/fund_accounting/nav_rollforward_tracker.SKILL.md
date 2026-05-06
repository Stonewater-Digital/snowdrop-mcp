---
skill: nav_rollforward_tracker
category: fund_accounting
description: Bridges opening NAV to closing NAV using period cash flows and valuation changes. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: opening_nav, cash_flows, valuation_change, management_fees, period_label
---

# Nav Rollforward Tracker

## Description
Bridges opening NAV to closing NAV using period cash flows and valuation changes. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `opening_nav` | `number` | Yes | NAV at the start of the reporting period in dollars. |
| `cash_flows` | `array` | Yes | List of cash flow objects for the period, each with `type` (`"call"` or `"distribution"`), `amount`, and `date`. |
| `valuation_change` | `number` | No | Net unrealized gain/loss in portfolio valuations for the period in dollars. Defaults to `0.0`. |
| `management_fees` | `number` | No | Management fees charged against NAV for the period in dollars. Defaults to `0.0`. |
| `period_label` | `string` | No | Human-readable period label (e.g. `"Q4 2025"`) used in the report output. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nav_rollforward_tracker",
  "arguments": {
    "opening_nav": 85000000,
    "cash_flows": [
      {"type": "call", "amount": 8000000, "date": "2025-10-15"},
      {"type": "distribution", "amount": -5000000, "date": "2025-12-01"}
    ],
    "valuation_change": 3200000,
    "management_fees": 425000,
    "period_label": "Q4 2025"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nav_rollforward_tracker"`.
