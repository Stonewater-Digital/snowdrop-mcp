---
skill: yield_curve_bootstrapper
category: fixed_income_analytics
description: Bootstraps spot and forward curves from par coupon instruments consistent with U.S. Treasury STRIPS methodology.
tier: premium
inputs: none
---

# Yield Curve Bootstrapper

## Description
Bootstraps spot and forward curves from par coupon instruments consistent with U.S. Treasury STRIPS methodology. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "yield_curve_bootstrapper",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "yield_curve_bootstrapper"`.
