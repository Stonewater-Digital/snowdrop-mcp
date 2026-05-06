---
skill: irr_bridge_reporter
category: investor_relations
description: Calculates IRR, DPI, RVPI, and TVPI along with driver bridge for investor reporting. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Irr Bridge Reporter

## Description
Calculates IRR, DPI, RVPI, and TVPI along with driver bridge for investor reporting. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "irr_bridge_reporter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "irr_bridge_reporter"`.
