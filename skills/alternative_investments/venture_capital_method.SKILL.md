---
skill: venture_capital_method
category: alternative_investments
description: Discounts exit value by target IRR, layers dilution, and solves for pre/post-money valuations per the VC method. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Venture Capital Method

## Description
Discounts exit value by target IRR, layers dilution, and solves for pre/post-money valuations per the VC method. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "venture_capital_method",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "venture_capital_method"`.
