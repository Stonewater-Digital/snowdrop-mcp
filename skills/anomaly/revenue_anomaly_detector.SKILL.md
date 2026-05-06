---
skill: revenue_anomaly_detector
category: anomaly
description: Monitors rolling revenue patterns for drops and spikes.
tier: free
inputs: daily_revenue
---

# Revenue Anomaly Detector

## Description
Monitors rolling revenue patterns for drops and spikes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_revenue` | `array` | Yes |  |
| `sensitivity` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "revenue_anomaly_detector",
  "arguments": {
    "daily_revenue": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "revenue_anomaly_detector"`.
