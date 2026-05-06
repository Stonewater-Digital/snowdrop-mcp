---
skill: gross_rent_multiplier_calculator
category: real_estate
description: Calculate gross rent multiplier (GRM = Property Price / Gross Annual Rent). Lower GRM generally indicates better value.
tier: free
inputs: property_price, gross_annual_rent
---

# Gross Rent Multiplier Calculator

## Description
Calculate gross rent multiplier (GRM = Property Price / Gross Annual Rent). Lower GRM generally indicates better value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `property_price` | `number` | Yes | Property purchase price in USD. |
| `gross_annual_rent` | `number` | Yes | Gross annual rental income in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gross_rent_multiplier_calculator",
  "arguments": {
    "property_price": 0,
    "gross_annual_rent": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gross_rent_multiplier_calculator"`.
