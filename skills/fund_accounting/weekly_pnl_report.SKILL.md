---
skill: weekly_pnl_report
category: fund_accounting
description: Aggregates revenue and expense items into a weekly P&L rollup. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Weekly Pnl Report

## Description
Aggregates revenue and expense items into a weekly P&L rollup. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "weekly_pnl_report",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "weekly_pnl_report"`.
