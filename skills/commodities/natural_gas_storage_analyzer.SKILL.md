---
skill: natural_gas_storage_analyzer
category: commodities
description: Compares EIA-style natural gas storage levels to 5-year seasonal averages, flags injection/withdrawal pace, and provides bullish/bearish market implication.
tier: free
inputs: storage_bcf, five_year_avg_bcf
---

# Natural Gas Storage Analyzer

## Description
Compares EIA-style natural gas storage levels to 5-year seasonal averages, flags injection/withdrawal pace, and provides bullish/bearish market implication.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `storage_bcf` | `number` | Yes | Current storage level in billion cubic feet (must be >= 0). |
| `five_year_avg_bcf` | `number` | Yes | 5-year seasonal average storage level in Bcf (must be > 0). |
| `five_year_max_bcf` | `['number', 'null']` | No | 5-year maximum storage at this date (optional, for range context). |
| `five_year_min_bcf` | `['number', 'null']` | No | 5-year minimum storage at this date (optional, for range context). |
| `daily_flow_bcf` | `number` | No | Net daily injection (+) or withdrawal (−) in Bcf/day. |
| `season_phase` | `string` | No | Current seasonal phase: 'injection' (Apr–Oct) or 'withdrawal' (Nov–Mar). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "natural_gas_storage_analyzer",
  "arguments": {
    "storage_bcf": 0,
    "five_year_avg_bcf": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "natural_gas_storage_analyzer"`.
