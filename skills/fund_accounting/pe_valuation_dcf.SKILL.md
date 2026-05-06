---
skill: pe_valuation_dcf
category: fund_accounting
description: Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Pe Valuation Dcf

## Description
Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "pe_valuation_dcf",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pe_valuation_dcf"`.
