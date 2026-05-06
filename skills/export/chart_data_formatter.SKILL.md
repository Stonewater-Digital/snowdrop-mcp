---
skill: chart_data_formatter
category: export
description: Normalizes data into Chart.js/Plotly friendly schema with labels/datasets.
tier: free
inputs: data, chart_type, x_field, y_fields, title
---

# Chart Data Formatter

## Description
Normalizes data into Chart.js/Plotly friendly schema with labels/datasets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `array` | Yes |  |
| `chart_type` | `string` | Yes |  |
| `x_field` | `string` | Yes |  |
| `y_fields` | `array` | Yes |  |
| `title` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "chart_data_formatter",
  "arguments": {
    "data": [],
    "chart_type": "<chart_type>",
    "x_field": "<x_field>",
    "y_fields": [],
    "title": "<title>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chart_data_formatter"`.
