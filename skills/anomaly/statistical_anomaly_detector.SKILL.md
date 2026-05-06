---
skill: statistical_anomaly_detector
category: anomaly
description: Flags z-score anomalies across global or rolling windows.
tier: free
inputs: values, labels
---

# Statistical Anomaly Detector

## Description
Flags z-score anomalies across global or rolling windows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `values` | `array` | Yes |  |
| `labels` | `array` | Yes |  |
| `z_threshold` | `number` | No |  |
| `window` | `['integer', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "statistical_anomaly_detector",
  "arguments": {
    "values": [],
    "labels": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "statistical_anomaly_detector"`.
