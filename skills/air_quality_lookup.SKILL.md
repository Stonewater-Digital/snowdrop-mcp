---
skill: air_quality_lookup
category: root
description: Retrieve current air quality conditions, historical hourly AQI data, or heatmap tile configuration for any location using the Google Air Quality API. Returns AQI score, dominant pollutant, individual pollutant concentrations, health recommendations, plus an esg_score (0–100) and real_estate_impact assessment for ESG reporting and property valuation workflows.
tier: free
inputs: action, location
---

# Air Quality Lookup

## Description
Retrieve current air quality conditions, historical hourly AQI data, or heatmap tile configuration for any location using the Google Air Quality API. Returns AQI score, dominant pollutant, individual pollutant concentrations, health recommendations, plus an esg_score (0–100) and real_estate_impact assessment for ESG reporting and property valuation workflows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Air quality operation to perform. |
| `location` | `string` | Yes | 'lat,lng' string or human-readable address. |
| `hours` | `integer` | No | Hours of historical AQI data to retrieve (history action). |
| `language_code` | `string` | No | BCP-47 language code for health recommendations text. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "air_quality_lookup",
  "arguments": {
    "action": "<action>",
    "location": "<location>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "air_quality_lookup"`.
