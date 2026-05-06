---
skill: us_state_ma_fund_tax
category: fund_tax
description: Calculates Massachusetts flat tax, millionaires surtax, and SALT workaround election under Mass. Gen.
tier: premium
inputs: none
---

# Us State Ma Fund Tax

## Description
Calculates Massachusetts flat tax, millionaires surtax, and SALT workaround election under Mass. Gen. Laws ch. 62 and ch. 63D. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ma_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ma_fund_tax"`.
