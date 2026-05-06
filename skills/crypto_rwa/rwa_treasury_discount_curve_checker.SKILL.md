---
skill: rwa_treasury_discount_curve_checker
category: crypto_rwa
description: Compares implied token discounts to the live Treasury curve to spot mispricing.
tier: free
inputs: none
---

# Rwa Treasury Discount Curve Checker

## Description
Compares implied token discounts to the live Treasury curve to spot mispricing.

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
  "tool": "rwa_treasury_discount_curve_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_discount_curve_checker"`.
