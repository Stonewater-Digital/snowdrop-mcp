---
skill: insurance_regulatory_checker
category: insurance_analytics
description: Checks NAIC Risk-Based Capital (RBC) ratio and NWP-to-surplus leverage against standard P&C regulatory thresholds. Returns action level classification, surplus adequacy assessment, and list of regulatory concerns.
tier: free
inputs: line_of_business, net_written_premium, policyholder_surplus, total_adjusted_capital, authorized_control_level_rbc
---

# Insurance Regulatory Checker

## Description
Checks NAIC Risk-Based Capital (RBC) ratio and NWP-to-surplus leverage against standard P&C regulatory thresholds. Returns action level classification, surplus adequacy assessment, and list of regulatory concerns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `line_of_business` | `string` | Yes | Primary line of business (e.g., 'Workers Compensation', 'Commercial Auto', 'Homeowners'). |
| `net_written_premium` | `number` | Yes | Annual net written premium. Must be >= 0. |
| `policyholder_surplus` | `number` | Yes | Total statutory policyholder surplus (net assets). May be negative (insolvency indicator). |
| `total_adjusted_capital` | `number` | Yes | Total Adjusted Capital (TAC) = policyholder surplus + Asset Valuation Reserve and other NAIC adjustments. Used as numerator in RBC ratio. Must be >= 0. |
| `authorized_control_level_rbc` | `number` | Yes | Authorized Control Level (ACL) RBC — the denominator of the NAIC RBC ratio. Typically = Company Action Level RBC / 2. Must be > 0. |
| `prior_year_surplus` | `number` | No | Prior year-end policyholder surplus for surplus change analysis. Optional. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "insurance_regulatory_checker",
  "arguments": {
    "line_of_business": "<line_of_business>",
    "net_written_premium": 0,
    "policyholder_surplus": 0,
    "total_adjusted_capital": 0,
    "authorized_control_level_rbc": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "insurance_regulatory_checker"`.
