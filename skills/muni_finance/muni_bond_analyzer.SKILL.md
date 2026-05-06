---
skill: muni_bond_analyzer
category: muni_finance
description: Computes tax-equivalent yield, breakeven rates, and annual savings for muni bonds.
tier: free
inputs: muni_yield, taxable_yield, federal_tax_rate
---

# Muni Bond Analyzer

## Description
Computes tax-equivalent yield, breakeven rates, and annual savings for muni bonds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `muni_yield` | `number` | Yes |  |
| `taxable_yield` | `number` | Yes |  |
| `federal_tax_rate` | `number` | Yes |  |
| `state_tax_rate` | `number` | No |  |
| `in_state` | `boolean` | No |  |
| `amt_subject` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "muni_bond_analyzer",
  "arguments": {
    "muni_yield": 0,
    "taxable_yield": 0,
    "federal_tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "muni_bond_analyzer"`.
