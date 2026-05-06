---
skill: max_drawdown_analyzer
category: risk
description: Computes maximum drawdown statistics from an equity curve.
tier: free
inputs: equity_curve
---

# Max Drawdown Analyzer

## Description
Computes portfolio drawdown depth, timing, and recovery diagnostics from a chronological equity curve. Identifies the largest peak-to-trough decline as a percentage, the index positions of the peak and trough, the recovery index (first point the portfolio regains the prior peak, or null if not yet recovered), and the current drawdown percentage from the most recent peak. Requires at least two positive portfolio values. Use to assess historical downside risk and recovery characteristics for a portfolio or strategy.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `equity_curve` | `array` | Yes | Ordered list of portfolio equity values as positive numbers (e.g. daily NAV or total value in USD). Must contain at least 2 values; all values must be positive. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

Data fields: `max_drawdown_pct` (largest peak-to-trough loss as a positive percentage), `peak_date_index`, `trough_date_index`, `recovery_date_index` (null if not recovered), `current_drawdown_pct`.

## Example
```json
{
  "tool": "max_drawdown_analyzer",
  "arguments": {
    "equity_curve": [100000, 110000, 108000, 95000, 87000, 92000, 105000, 112000, 110000]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "max_drawdown_analyzer"`.
