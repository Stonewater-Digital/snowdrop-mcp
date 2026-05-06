---
skill: supply_chain_risk_insurance_model
category: corporate_insurance
description: Scores suppliers and calculates contingent BI exposure.
tier: free
inputs: suppliers
---

# Supply Chain Risk Insurance Model

## Description
Scores suppliers and calculates contingent BI exposure.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `suppliers` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "supply_chain_risk_insurance_model",
  "arguments": {
    "suppliers": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "supply_chain_risk_insurance_model"`.
