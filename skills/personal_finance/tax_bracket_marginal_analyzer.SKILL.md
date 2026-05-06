---
skill: tax_bracket_marginal_analyzer
category: personal_finance
description: Reports the taxpayer's current federal bracket, marginal rate, remaining income headroom before the next bracket, and a visualization of all bracket tiers.
tier: free
inputs: taxable_income, filing_status
---

# Tax Bracket Marginal Analyzer

## Description
Reports the taxpayer's current federal bracket, marginal rate, remaining income headroom before the next bracket, and a visualization of all bracket tiers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `taxable_income` | `number` | Yes | Income after deductions subject to federal tax. |
| `filing_status` | `string` | Yes | single or mfj. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tax_bracket_marginal_analyzer",
  "arguments": {
    "taxable_income": 0,
    "filing_status": "<filing_status>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_bracket_marginal_analyzer"`.
