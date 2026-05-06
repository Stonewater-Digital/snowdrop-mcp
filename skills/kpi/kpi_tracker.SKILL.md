---
skill: kpi_tracker
category: kpi
description: Calculates KPI progress, highlights off-track metrics, and summarizes health.
tier: free
inputs: kpis, period
---

# Kpi Tracker

## Description
Calculates KPI progress, highlights off-track metrics, and summarizes health.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `kpis` | `array` | Yes |  |
| `period` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "kpi_tracker",
  "arguments": {
    "kpis": [],
    "period": "<period>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "kpi_tracker"`.
