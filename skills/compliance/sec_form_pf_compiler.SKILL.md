---
skill: sec_form_pf_compiler
category: compliance
description: Compiles SEC Form PF data for private fund advisers under Dodd-Frank Act Section 404 and SEC Rule 204(b)-1. Determines Large Adviser classification, filing frequency, and generates the structured Form PF JSON payload for PFRD submission.
tier: premium
inputs: fund_data
---

# Sec Form Pf Compiler

## Description
Compiles SEC Form PF data for private fund advisers under Dodd-Frank Act Section 404 and SEC Rule 204(b)-1. Determines Large Adviser classification, filing frequency, and generates the structured Form PF JSON payload for PFRD submission. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_data` | `object` | Yes | Private fund adviser data including AUM, fund type (hedge/PE/liquidity), investor count, leverage ratios, and filing period for Form PF PFRD submission |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sec_form_pf_compiler",
  "arguments": {
    "fund_data": {
      "adviser_name": "Stonewater Capital LP",
      "total_aum_usd": 2500000000,
      "fund_type": "hedge_fund",
      "reporting_period": "2026-Q1",
      "investor_count": 145
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sec_form_pf_compiler"`.
