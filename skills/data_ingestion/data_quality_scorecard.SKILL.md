---
skill: data_quality_scorecard
category: data_ingestion
description: Compute null/duplication/freshness scores for administrator datasets and flag breaches.
tier: free
inputs: datasets
---

# Data Quality Scorecard

## Description
Compute null/duplication/freshness scores for administrator datasets and flag breaches.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `datasets` | `array` | Yes | Dataset payloads with keys: name, row_count, null_counts, duplicate_rows, last_refresh. |
| `thresholds` | `object` | No | Overrides for max_null_pct, max_dup_pct, max_staleness_minutes. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "data_quality_scorecard",
  "arguments": {
    "datasets": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "data_quality_scorecard"`.
