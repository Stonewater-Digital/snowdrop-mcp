---
skill: inflation_deflation_tracker
category: tokenomics
description: Computes inflation rates and estimates deflation crossover dates.
tier: free
inputs: supply_snapshots, burn_rate_daily, mint_rate_daily
---

# Inflation Deflation Tracker

## Description
Computes inflation rates and estimates deflation crossover dates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `supply_snapshots` | `array` | Yes |  |
| `burn_rate_daily` | `number` | Yes |  |
| `mint_rate_daily` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "inflation_deflation_tracker",
  "arguments": {
    "supply_snapshots": [],
    "burn_rate_daily": 0,
    "mint_rate_daily": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inflation_deflation_tracker"`.
