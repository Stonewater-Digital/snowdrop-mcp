---
skill: rwa_real_estate_property_tax_ledger_matcher
category: crypto_rwa
description: Matches property tax receipts versus blockchain cash flows to confirm taxes remain current.
tier: free
inputs: none
---

# Rwa Real Estate Property Tax Ledger Matcher

## Description
Matches property tax receipts versus blockchain cash flows to confirm taxes remain current.

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
  "tool": "rwa_real_estate_property_tax_ledger_matcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_property_tax_ledger_matcher"`.
