---
skill: australia_asics_checker
category: compliance
description: Determines Australian Financial Services Licence (AFSL) requirements under the Corporations Act 2001 (Cth) Part 7.6. Evaluates service type, client classification (retail vs wholesale), product categories, and foreign provider relief under ASIC Class Orders and legislative instruments.
tier: premium
inputs: entity_data
---

# Australia Asics Checker

## Description
Determines Australian Financial Services Licence (AFSL) requirements under the Corporations Act 2001 (Cth) Part 7.6. Evaluates service type, client classification (retail vs wholesale), product categories, and foreign provider relief under ASIC Class Orders and legislative instruments. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_data` | `object` | Yes | Entity details including service type, client classification (retail vs wholesale), and product categories for AFSL assessment |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "australia_asics_checker",
  "arguments": {
    "entity_data": {
      "service_type": "managed_discretionary_account",
      "client_type": "retail",
      "product_categories": ["equities", "derivatives"]
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "australia_asics_checker"`.
