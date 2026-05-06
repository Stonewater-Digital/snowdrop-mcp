---
skill: beta_calculator
category: market_analytics
description: Computes beta, correlation, alpha, systematic contribution, and residual risk relative to a benchmark.
tier: free
inputs: asset_returns, market_returns
---

# Beta Calculator

## Description
Computes beta, correlation, alpha, systematic contribution, and residual risk relative to a benchmark.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_returns` | `array` | Yes | Asset return series. |
| `market_returns` | `array` | Yes | Benchmark return series. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "beta_calculator",
  "arguments": {
    "asset_returns": [],
    "market_returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "beta_calculator"`.
