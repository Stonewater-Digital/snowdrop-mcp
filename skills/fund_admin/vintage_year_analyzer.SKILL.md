---
skill: vintage_year_analyzer
category: fund_admin
description: Benchmarks fund IRR/MOIC/DPI against vintage-year peer quartile data. Returns quartile placement (top/2nd/3rd/bottom) for each metric.
tier: premium
inputs: fund_metrics, peer_quartiles
---

# Vintage Year Analyzer

## Description
Benchmarks fund IRR/MOIC/DPI against vintage-year peer quartile data. Returns quartile placement (top/2nd/3rd/bottom) for each metric. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| fund_metrics | object | Yes | Dictionary of the fund's actual performance metrics keyed by metric name (e.g. `{"irr": 15.2, "moic": 2.1, "dpi": 0.85}`) |
| peer_quartiles | object | Yes | Dictionary of peer quartile breakpoints keyed by metric name; each value is an object with `q1`, `median`, and `q3` keys representing top-quartile, median, and third-quartile thresholds |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vintage_year_analyzer",
  "arguments": {
    "fund_metrics": {
      "irr": 15.2,
      "moic": 2.1,
      "dpi": 0.85
    },
    "peer_quartiles": {
      "irr": {"q1": 16.0, "median": 12.5, "q3": 9.0},
      "moic": {"q1": 2.2, "median": 1.8, "q3": 1.4},
      "dpi": {"q1": 1.0, "median": 0.75, "q3": 0.45}
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vintage_year_analyzer"`.
