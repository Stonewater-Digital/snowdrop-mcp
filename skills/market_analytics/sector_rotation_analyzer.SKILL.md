---
skill: sector_rotation_analyzer
category: market_analytics
description: Measures sector relative strength and assigns rotation phases (leading/lagging/etc.).
tier: free
inputs: sector_returns, benchmark_returns
---

# Sector Rotation Analyzer

## Description
Measures sector relative strength and assigns rotation phases (leading/lagging/etc.).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sector_returns` | `object` | Yes | Mapping of sector name to return list. |
| `benchmark_returns` | `array` | Yes | Benchmark return series. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sector_rotation_analyzer",
  "arguments": {
    "sector_returns": {},
    "benchmark_returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sector_rotation_analyzer"`.
