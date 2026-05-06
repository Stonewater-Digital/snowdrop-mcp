---
skill: environmental_liability_exposure_model
category: corporate_insurance
description: Estimates environmental liability exposure using scenario severities.
tier: free
inputs: cleanup_cost, third_party_liability, regulatory_fines, probability_pct
---

# Environmental Liability Exposure Model

## Description
Estimates environmental liability exposure using scenario severities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cleanup_cost` | `number` | Yes |  |
| `third_party_liability` | `number` | Yes |  |
| `regulatory_fines` | `number` | Yes |  |
| `probability_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "environmental_liability_exposure_model",
  "arguments": {
    "cleanup_cost": 0,
    "third_party_liability": 0,
    "regulatory_fines": 0,
    "probability_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "environmental_liability_exposure_model"`.
