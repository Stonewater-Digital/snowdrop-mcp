---
skill: rwa_servicer_quality_scorer
category: rwa_tokenization
description: Generates a composite score for RWA servicers using accuracy, staffing, and remittance metrics.
tier: free
inputs: error_rate_pct, remittance_days, staff_tenure_years, systems_uptime_pct
---

# Rwa Servicer Quality Scorer

## Description
Generates a composite score for RWA servicers using accuracy, staffing, and remittance metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `error_rate_pct` | `number` | Yes | Servicing error rate percent |
| `remittance_days` | `number` | Yes | Average days to remit cash |
| `staff_tenure_years` | `number` | Yes | Average staff tenure |
| `systems_uptime_pct` | `number` | Yes | Servicing platform uptime percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_servicer_quality_scorer",
  "arguments": {
    "error_rate_pct": 0,
    "remittance_days": 0,
    "staff_tenure_years": 0,
    "systems_uptime_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_servicer_quality_scorer"`.
