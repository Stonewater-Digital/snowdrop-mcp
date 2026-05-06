---
skill: catastrophe_bond_spreads
category: structured_products
description: Applies industry convention (expected loss + risk load + liquidity premium) to decompose cat bond spreads. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Catastrophe Bond Spreads

## Description
Applies industry convention (expected loss + risk load + liquidity premium) to decompose cat bond spreads. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "catastrophe_bond_spreads",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "catastrophe_bond_spreads"`.
