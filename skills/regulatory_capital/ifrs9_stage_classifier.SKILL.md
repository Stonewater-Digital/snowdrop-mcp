---
skill: ifrs9_stage_classifier
category: regulatory_capital
description: Classifies assets into IFRS 9 stages using PD migration and delinquency criteria.
tier: free
inputs: origination_pd, current_pd, sicr_threshold_pct, dpd_days, qualitative_triggers
---

# Ifrs9 Stage Classifier

## Description
Classifies assets into IFRS 9 stages using PD migration and delinquency criteria.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `origination_pd` | `number` | Yes | PD at origination (decimal). |
| `current_pd` | `number` | Yes | Current PD (decimal). |
| `sicr_threshold_pct` | `number` | Yes | SICR threshold as % increase. |
| `dpd_days` | `integer` | Yes | Days past due. |
| `qualitative_triggers` | `array` | Yes | List of qualitative factors (e.g., watchlist). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ifrs9_stage_classifier",
  "arguments": {
    "origination_pd": 0,
    "current_pd": 0,
    "sicr_threshold_pct": 0,
    "dpd_days": 0,
    "qualitative_triggers": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ifrs9_stage_classifier"`.
