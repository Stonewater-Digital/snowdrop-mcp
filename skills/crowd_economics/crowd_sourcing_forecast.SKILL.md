---
skill: crowd_sourcing_forecast
category: crowd_economics
description: Projects contributions, skills, and value under bear/base/bull scenarios for six months.
tier: free
inputs: historical, growth_scenarios
---

# Crowd Sourcing Forecast

## Description
Projects contributions, skills, and value under bear/base/bull scenarios for six months.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `historical` | `array` | Yes |  |
| `growth_scenarios` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "crowd_sourcing_forecast",
  "arguments": {
    "historical": [],
    "growth_scenarios": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crowd_sourcing_forecast"`.
