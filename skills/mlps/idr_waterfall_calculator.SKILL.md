---
skill: idr_waterfall_calculator
category: mlps
description: Allocates distributable cash through IDR tiers for MLPs. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Idr Waterfall Calculator

## Description
Allocates distributable cash through IDR tiers for MLPs. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "idr_waterfall_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "idr_waterfall_calculator"`.
