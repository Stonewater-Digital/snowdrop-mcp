---
skill: max_drawdown_analyzer
category: risk
description: Computes maximum drawdown statistics from an equity curve.
tier: free
inputs: equity_curve
---

# Max Drawdown Analyzer

## Description
Computes maximum drawdown statistics from an equity curve.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `equity_curve` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "max_drawdown_analyzer",
  "arguments": {
    "equity_curve": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "max_drawdown_analyzer"`.
