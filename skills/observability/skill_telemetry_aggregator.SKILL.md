---
skill: skill_telemetry_aggregator
category: observability
description: Process telemetry samples from Snowdrop skills and emit aggregated health metrics with outlier detection.
tier: free
inputs: metrics
---

# Skill Telemetry Aggregator

## Description
Process telemetry samples from Snowdrop skills and emit aggregated health metrics with outlier detection.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `metrics` | `array` | Yes | Telemetry samples containing at least skill_name, latency_ms, status, timestamp. |
| `window_minutes` | `integer` | No | Only samples within this lookback window are considered. |
| `error_threshold_pct` | `number` | No | Error rate percentage that triggers an outlier flag. |
| `notify_on_outliers` | `boolean` | No | Send Thunder alerts via thunder_signal when outliers appear. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_telemetry_aggregator",
  "arguments": {
    "metrics": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_telemetry_aggregator"`.
