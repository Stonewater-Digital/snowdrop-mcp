---
skill: rwa_real_estate_property_tax_ledger_matcher
category: crypto_rwa
description: Matches property tax receipts versus blockchain cash flows to confirm taxes remain current.
tier: free
inputs: payload
---

# Rwa Real Estate Property Tax Ledger Matcher

## Description
Matches property tax receipts versus blockchain cash flows to confirm taxes remain current.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_property_tax_ledger_matcher",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_property_tax_ledger_matcher"`.
