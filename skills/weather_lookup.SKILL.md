---
skill: weather_lookup
category: root
description: Fetch current weather, multi-day forecasts, or historical weather data for any location using the Google Weather API. Returns structured weather metrics plus a commodity_signal field flagging weather-driven market implications for agricultural futures and supply chain analysis.
tier: free
inputs: action, location
---

# Weather Lookup

## Description
Fetch current weather, multi-day forecasts, or historical weather data for any location using the Google Weather API. Returns structured weather metrics plus a commodity_signal field flagging weather-driven market implications for agricultural futures and supply chain analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Weather operation to perform. |
| `location` | `string` | Yes | City name, full address, or 'lat,lng' string. |
| `days` | `integer` | No | Number of forecast days (forecast action only). |
| `hours` | `integer` | No | Hours of historical data to retrieve (history action only). |
| `units` | `string` | No | Unit system for temperature and wind speed. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "weather_lookup",
  "arguments": {
    "action": "<action>",
    "location": "<location>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "weather_lookup"`.
