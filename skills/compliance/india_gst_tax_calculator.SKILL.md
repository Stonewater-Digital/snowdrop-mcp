---
skill: india_gst_tax_calculator
category: compliance
description: Calculates Indian Goods and Services Tax (GST) for services including cross-border supply, SEZ, and export scenarios. Applies IGST Act 2017 rates, OIDAR (Online Information Database Access and Retrieval) rules, and LUT (Letter of Undertaking) exemptions for zero-rated exports.
tier: free
inputs: service_type, service_value_inr, recipient_location, is_oidar
---

# India Gst Tax Calculator

## Description
Calculates Indian Goods and Services Tax (GST) for services including cross-border supply, SEZ, and export scenarios. Applies IGST Act 2017 rates, OIDAR (Online Information Database Access and Retrieval) rules, and LUT (Letter of Undertaking) exemptions for zero-rated exports.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `service_type` | `string` | Yes | Type of service: financial_services / software / consulting / cloud / data_analytics / fintech / other |
| `service_value_inr` | `number` | Yes | Transaction value in Indian Rupees (INR) |
| `recipient_location` | `string` | Yes | Recipient jurisdiction: 'domestic' / 'sez' (Special Economic Zone) / 'export' (outside India) |
| `is_oidar` | `boolean` | Yes | True if the service is Online Information Database Access and Retrieval (OIDAR) |
| `has_lut` | `boolean` | No | True if a valid Letter of Undertaking (LUT) is filed with GST authority (required for zero-rated export without paying IGST) |
| `recipient_is_registered` | `boolean` | No | True if the domestic recipient is a GST-registered business (B2B vs B2C changes reverse charge applicability) |
| `state_of_supplier` | `string` | No | State code of the supplier (for CGST/SGST vs IGST determination, e.g. 'MH', 'KA', 'DL') |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "india_gst_tax_calculator",
  "arguments": {
    "service_type": "<service_type>",
    "service_value_inr": 0,
    "recipient_location": "<recipient_location>",
    "is_oidar": false
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "india_gst_tax_calculator"`.
