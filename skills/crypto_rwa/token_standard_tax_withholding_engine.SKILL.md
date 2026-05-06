---
skill: token_standard_tax_withholding_engine
category: crypto_rwa
description: Calculates withholding schedules per jurisdiction before stablecoin payouts.
tier: free
inputs: none
---

# Token Standard Tax Withholding Engine

## Description
Calculates withholding schedules per jurisdiction before stablecoin payouts.

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
  "tool": "token_standard_tax_withholding_engine",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_tax_withholding_engine"`.
