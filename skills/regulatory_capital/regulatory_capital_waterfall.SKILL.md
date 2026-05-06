---
skill: regulatory_capital_waterfall
category: regulatory_capital
description: Applies deductions to CET1 and adds AT1/Tier2 to produce regulatory ratios.
tier: free
inputs: gross_cet1, regulatory_deductions, at1_instruments, tier2_instruments, rwa
---

# Regulatory Capital Waterfall

## Description
Applies deductions to CET1 and adds AT1/Tier2 to produce regulatory ratios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_cet1` | `number` | Yes | Gross CET1 capital before deductions. |
| `regulatory_deductions` | `number` | Yes | Total deductions (goodwill, DTAs, etc.). |
| `at1_instruments` | `number` | Yes | Eligible AT1 capital. |
| `tier2_instruments` | `number` | Yes | Eligible Tier 2 capital. |
| `rwa` | `number` | Yes | Risk-weighted assets. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "regulatory_capital_waterfall",
  "arguments": {
    "gross_cet1": 0,
    "regulatory_deductions": 0,
    "at1_instruments": 0,
    "tier2_instruments": 0,
    "rwa": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "regulatory_capital_waterfall"`.
