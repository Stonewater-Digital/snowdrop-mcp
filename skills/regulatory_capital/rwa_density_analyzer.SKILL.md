---
skill: rwa_density_analyzer
category: regulatory_capital
description: Computes RWA/exposure percentages and flags segments deviating from portfolio average.
tier: free
inputs: segments
---

# Rwa Density Analyzer

## Description
Computes RWA/exposure percentages and flags segments deviating from portfolio average.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `segments` | `array` | Yes | List of segments with exposure and RWA amounts. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_density_analyzer",
  "arguments": {
    "segments": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_density_analyzer"`.
