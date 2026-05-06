---
skill: cds_hazard_rate_bootstrapper
category: credit_default_swaps
description: Bootstraps hazard rates from CDS spreads and recovery assumptions.
tier: free
inputs: spreads_bps, tenors_years
---

# Cds Hazard Rate Bootstrapper

## Description
Bootstraps hazard rates from CDS spreads and recovery assumptions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spreads_bps` | `array` | Yes |  |
| `tenors_years` | `array` | Yes |  |
| `recovery_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_hazard_rate_bootstrapper",
  "arguments": {
    "spreads_bps": [],
    "tenors_years": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_hazard_rate_bootstrapper"`.
