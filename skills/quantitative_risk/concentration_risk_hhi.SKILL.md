---
skill: concentration_risk_hhi
category: quantitative_risk
description: Computes HHI, effective number of obligors, and top exposures akin to ECB concentration add-ons.
tier: free
inputs: exposures
---

# Concentration Risk Hhi

## Description
Computes HHI, effective number of obligors, and top exposures akin to ECB concentration add-ons.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes | Exposure list with obligor name and amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "concentration_risk_hhi",
  "arguments": {
    "exposures": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "concentration_risk_hhi"`.
