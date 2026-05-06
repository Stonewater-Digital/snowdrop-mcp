---
skill: withholding_tax_reclaim_tracker
category: fund_tax
description: Summarizes reclaimable withholding tax amounts and filing deadlines per country. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Withholding Tax Reclaim Tracker

## Description
Summarizes reclaimable withholding tax amounts and filing deadlines per country. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "withholding_tax_reclaim_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "withholding_tax_reclaim_tracker"`.
