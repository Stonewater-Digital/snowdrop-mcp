---
skill: cre_lease_comparator
category: cre
description: Evaluates tenant/landlord economics for NNN, gross, and modified gross leases.
tier: free
inputs: base_rent_psf, rentable_sqft, opex_psf, cam_psf, insurance_psf, tax_psf, annual_escalation_pct, lease_term_years, ti_allowance_psf, free_rent_months
---

# Cre Lease Comparator

## Description
Evaluates tenant/landlord economics for NNN, gross, and modified gross leases.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_rent_psf` | `number` | Yes |  |
| `rentable_sqft` | `integer` | Yes |  |
| `opex_psf` | `number` | Yes |  |
| `cam_psf` | `number` | Yes |  |
| `insurance_psf` | `number` | Yes |  |
| `tax_psf` | `number` | Yes |  |
| `annual_escalation_pct` | `number` | Yes |  |
| `lease_term_years` | `integer` | Yes |  |
| `ti_allowance_psf` | `number` | Yes |  |
| `free_rent_months` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cre_lease_comparator",
  "arguments": {
    "base_rent_psf": 0,
    "rentable_sqft": 0,
    "opex_psf": 0,
    "cam_psf": 0,
    "insurance_psf": 0,
    "tax_psf": 0,
    "annual_escalation_pct": 0,
    "lease_term_years": 0,
    "ti_allowance_psf": 0,
    "free_rent_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cre_lease_comparator"`.
