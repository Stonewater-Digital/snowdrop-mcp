---
skill: amt_calculator
category: personal_finance
description: Calculates Alternative Minimum Tax income, exemption phase-out, tentative minimum tax, and resulting liability versus the regular tax system.
tier: free
inputs: regular_taxable_income, amt_preference_items, filing_status
---

# Amt Calculator

## Description
Calculates Alternative Minimum Tax income, exemption phase-out, tentative minimum tax, and resulting liability versus the regular tax system.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `regular_taxable_income` | `number` | Yes | Taxable income under regular rules. |
| `amt_preference_items` | `array` | Yes | List of AMT add-backs (ISO spreads, state tax, etc.). |
| `filing_status` | `string` | Yes | single or mfj. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "amt_calculator",
  "arguments": {
    "regular_taxable_income": 0,
    "amt_preference_items": [],
    "filing_status": "<filing_status>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "amt_calculator"`.
