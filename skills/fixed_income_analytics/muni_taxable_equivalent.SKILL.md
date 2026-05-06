---
skill: muni_taxable_equivalent
category: fixed_income_analytics
description: Computes taxable-equivalent yields for tax-exempt municipal bonds incorporating AMT exposure, state deductibility, and the 3.8% Medicare net investment income surtax. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Muni Taxable Equivalent

## Description
Computes taxable-equivalent yields for tax-exempt municipal bonds incorporating AMT exposure, state deductibility, and the 3.8% Medicare net investment income surtax. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "muni_taxable_equivalent",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "muni_taxable_equivalent"`.
