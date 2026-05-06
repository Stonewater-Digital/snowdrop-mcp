---
skill: global_tax_withholding_skill
category: technical
description: Calculates the withholding tax on a distribution to an international LP. Applies any available tax treaty rate in preference to the default rate.
tier: free
inputs: lp_data, withholding_rates
---

# Global Tax Withholding Skill

## Description
Calculates the withholding tax on a distribution to an international LP. Applies any available tax treaty rate in preference to the default rate. Grants full exemption (0%) to qualifying entities such as pension funds and sovereign wealth funds. Returns the withholding amount, effective rate, and net distribution after withholding.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lp_data` | `object` | Yes |  |
| `withholding_rates` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "global_tax_withholding_skill",
  "arguments": {
    "lp_data": {},
    "withholding_rates": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "global_tax_withholding_skill"`.
