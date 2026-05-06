---
skill: max_drawdown_analyzer
category: market_analytics
description: Computes drawdown statistics, including top drawdowns and recovery metrics.
tier: free
inputs: prices
---

# Max Drawdown Analyzer

## Description
Computes drawdown statistics, including top drawdowns and recovery metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Equity curve or price series. |

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
    "prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "max_drawdown_analyzer"`.
