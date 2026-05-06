---
skill: rwa_originator_quality_scorer
category: rwa_tokenization
description: Combines historical loss rates, audits, and reporting cadence into an originator score.
tier: free
inputs: years_operating, cumulative_loss_rate_pct, audit_rating_pct, reporting_timeliness_score
---

# Rwa Originator Quality Scorer

## Description
Combines historical loss rates, audits, and reporting cadence into an originator score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `years_operating` | `number` | Yes | Years in operation |
| `cumulative_loss_rate_pct` | `number` | Yes | Historical loss rate |
| `audit_rating_pct` | `number` | Yes | Audit quality percent |
| `reporting_timeliness_score` | `number` | Yes | Score 0-100 for reporting timeliness |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_originator_quality_scorer",
  "arguments": {
    "years_operating": 0,
    "cumulative_loss_rate_pct": 0,
    "audit_rating_pct": 0,
    "reporting_timeliness_score": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_originator_quality_scorer"`.
