---
skill: rwa_treasury_safekeeping_receipt_checker
category: crypto_rwa
description: Validates safekeeping receipts and custodial chain-of-control for token wrappers.
tier: free
inputs: none
---

# Rwa Treasury Safekeeping Receipt Checker

## Description
Validates safekeeping receipts and custodial chain-of-control for token wrappers.

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
  "tool": "rwa_treasury_safekeeping_receipt_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_safekeeping_receipt_checker"`.
