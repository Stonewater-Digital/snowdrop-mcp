---
skill: farmland_valuation
category: alternative_investments
description: Capitalizes normalized NOI per acre and blends with comparable sale metrics to determine farmland value. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Farmland Valuation

## Description
Capitalizes normalized NOI per acre and blends with comparable sale metrics to determine farmland value. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "farmland_valuation",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "farmland_valuation"`.
