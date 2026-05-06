---
skill: facility_amendment_fee_calculator
category: private_credit
description: Computes amendment consent fees based on participation levels.
tier: free
inputs: facility_size, consent_obtained_pct, required_consent_pct, base_fee_bps
---

# Facility Amendment Fee Calculator

## Description
Computes amendment consent fees based on participation levels.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `facility_size` | `number` | Yes |  |
| `consent_obtained_pct` | `number` | Yes |  |
| `required_consent_pct` | `number` | Yes |  |
| `base_fee_bps` | `number` | Yes |  |
| `incentive_fee_bps` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "facility_amendment_fee_calculator",
  "arguments": {
    "facility_size": 0,
    "consent_obtained_pct": 0,
    "required_consent_pct": 0,
    "base_fee_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "facility_amendment_fee_calculator"`.
