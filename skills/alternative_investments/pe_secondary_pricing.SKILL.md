---
skill: pe_secondary_pricing
category: alternative_investments
description: Applies secondary market heuristics (quartile + remaining commitment) to derive bid discount and implied IRR. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Pe Secondary Pricing

## Description
Applies secondary market heuristics (quartile + remaining commitment) to derive bid discount and implied IRR. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "pe_secondary_pricing",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pe_secondary_pricing"`.
