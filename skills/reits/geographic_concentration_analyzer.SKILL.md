---
skill: geographic_concentration_analyzer
category: reits
description: Calculates HHI by region and flags concentration against limits.
tier: free
inputs: exposures
---

# Geographic Concentration Analyzer

## Description
Calculates HHI by region and flags concentration against limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes |  |
| `limit_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "geographic_concentration_analyzer",
  "arguments": {
    "exposures": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "geographic_concentration_analyzer"`.
