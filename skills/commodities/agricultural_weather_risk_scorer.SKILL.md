---
skill: agricultural_weather_risk_scorer
category: commodities
description: Scores crop yield risk from precipitation and temperature anomalies across agricultural regions. Returns risk scores (0–10), identifies the highest-risk region, and provides an aggregate supply disruption probability estimate.
tier: free
inputs: regions
---

# Agricultural Weather Risk Scorer

## Description
Scores crop yield risk from precipitation and temperature anomalies across agricultural regions. Returns risk scores (0–10), identifies the highest-risk region, and provides an aggregate supply disruption probability estimate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `regions` | `array` | Yes | List of regions with weather anomaly data. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agricultural_weather_risk_scorer",
  "arguments": {
    "regions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agricultural_weather_risk_scorer"`.
