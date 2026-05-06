---
skill: dupont_analysis_calculator
category: accounting
description: Performs DuPont analysis, decomposing return on equity into net profit margin, asset turnover, and equity multiplier (ROE = NPM x AT x EM).
tier: free
inputs: net_income, revenue, total_assets, total_equity
---

# Dupont Analysis Calculator

## Description
Performs DuPont analysis, decomposing return on equity into net profit margin, asset turnover, and equity multiplier (ROE = NPM x AT x EM).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | Net income for the period. |
| `revenue` | `number` | Yes | Total revenue. |
| `total_assets` | `number` | Yes | Total assets. |
| `total_equity` | `number` | Yes | Total shareholders equity. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dupont_analysis_calculator",
  "arguments": {
    "net_income": 0,
    "revenue": 0,
    "total_assets": 0,
    "total_equity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dupont_analysis_calculator"`.
