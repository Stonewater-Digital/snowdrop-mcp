---
skill: credit_conversion_factor_calculator
category: regulatory_capital
description: Assigns Basel CCF based on facility type (commitment, guarantee, trade finance, etc.).
tier: free
inputs: facility_type, drawn_amount, undrawn_commitment, regulatory_category
---

# Credit Conversion Factor Calculator

## Description
Assigns Basel CCF based on facility type (commitment, guarantee, trade finance, etc.).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `facility_type` | `string` | Yes | Facility description. |
| `drawn_amount` | `number` | Yes | Outstandings. |
| `undrawn_commitment` | `number` | Yes | Unused line amount. |
| `regulatory_category` | `string` | Yes | Basel category (e.g., irrevocable_commitment, performance_guarantee). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_conversion_factor_calculator",
  "arguments": {
    "facility_type": "<facility_type>",
    "drawn_amount": 0,
    "undrawn_commitment": 0,
    "regulatory_category": "<regulatory_category>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_conversion_factor_calculator"`.
