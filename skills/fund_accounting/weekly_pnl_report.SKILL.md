---
skill: weekly_pnl_report
category: fund_accounting
description: Aggregates revenue and expense items into a weekly P&L rollup. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: revenue_items, expense_items, period_start, period_end
---

# Weekly Pnl Report

## Description
Aggregates revenue and expense items into a weekly P&L rollup. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revenue_items` | `array` | Yes | List of revenue line item objects, each with `description`, `amount`, and optionally `category` (e.g. `"interest_income"`, `"dividend"`, `"realized_gain"`). |
| `expense_items` | `array` | Yes | List of expense line item objects, each with `description`, `amount`, and optionally `category` (e.g. `"management_fee"`, `"legal"`, `"admin"`). |
| `period_start` | `string` | Yes | ISO 8601 start date of the weekly reporting period (e.g. `"2026-04-28"`). |
| `period_end` | `string` | Yes | ISO 8601 end date of the weekly reporting period (e.g. `"2026-05-04"`). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "weekly_pnl_report",
  "arguments": {
    "revenue_items": [
      {"description": "Interest income - Mercury savings", "amount": 3850.00, "category": "interest_income"},
      {"description": "Realized gain - BTC sale", "amount": 12400.00, "category": "realized_gain"}
    ],
    "expense_items": [
      {"description": "Legal review - LP subscription docs", "amount": 4200.00, "category": "legal"},
      {"description": "Cloud infrastructure (GCP)", "amount": 380.00, "category": "admin"}
    ],
    "period_start": "2026-04-28",
    "period_end": "2026-05-04"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "weekly_pnl_report"`.
