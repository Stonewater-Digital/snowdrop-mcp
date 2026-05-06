---
skill: dashboard_aggregator
category: kpi
description: Groups panels by source, surfaces alerts, and crafts summary sentences.
tier: free
inputs: panels
---

# Dashboard Aggregator

## Description
Groups panels by source, surfaces alerts, and crafts summary sentences.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `panels` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dashboard_aggregator",
  "arguments": {
    "panels": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dashboard_aggregator"`.
