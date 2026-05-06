---
skill: operational_maturity_scorer
category: readiness
description: Rates capabilities across dimensions and assigns an overall maturity level.
tier: free
inputs: dimensions
---

# Operational Maturity Scorer

## Description
Rates capabilities across dimensions and assigns an overall maturity level.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dimensions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "operational_maturity_scorer",
  "arguments": {
    "dimensions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "operational_maturity_scorer"`.
