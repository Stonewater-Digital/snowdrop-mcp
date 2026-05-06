---
skill: portfolio_optimization_tool
category: quant
description: Builds heuristic mean-variance weights using return expectations and volatilities.
tier: free
inputs: assets
---

# Portfolio Optimization Tool

## Description
Builds heuristic mean-variance weights using return expectations and volatilities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `array` | Yes |  |
| `risk_free_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_optimization_tool",
  "arguments": {
    "assets": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_optimization_tool"`.
