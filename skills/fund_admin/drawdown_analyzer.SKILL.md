---
skill: drawdown_analyzer
category: fund_admin
description: Computes drawdown metrics from an equity curve or NAV series. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: equity_curve, period_label
---

# Drawdown Analyzer

## Description
Computes drawdown metrics from an equity curve or NAV series. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| equity_curve | array | Yes | Ordered list of NAV or equity values representing the fund's value over time (e.g. quarterly NAV snapshots) |
| period_label | string | No | Label describing the frequency of data points for reporting purposes (e.g. "quarterly", "monthly", "daily"; default: "daily") |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "drawdown_analyzer",
  "arguments": {
    "equity_curve": [100000000, 108000000, 115000000, 102000000, 95000000, 99000000, 112000000, 130000000],
    "period_label": "quarterly"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "drawdown_analyzer"`.
