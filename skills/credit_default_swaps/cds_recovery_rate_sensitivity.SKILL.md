---
skill: cds_recovery_rate_sensitivity
category: credit_default_swaps
description: Analyzes CDS spread sensitivity to recovery rate scenarios.
tier: free
inputs: base_spread_bps, recovery_scenarios_pct, default_probability_pct
---

# Cds Recovery Rate Sensitivity

## Description
Analyzes CDS spread sensitivity to recovery rate scenarios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_spread_bps` | `number` | Yes |  |
| `recovery_scenarios_pct` | `array` | Yes |  |
| `default_probability_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_recovery_rate_sensitivity",
  "arguments": {
    "base_spread_bps": 0,
    "recovery_scenarios_pct": [],
    "default_probability_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_recovery_rate_sensitivity"`.
