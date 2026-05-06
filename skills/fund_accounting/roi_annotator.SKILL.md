---
skill: roi_annotator
category: fund_accounting
description: Enriches ledger transactions with qualitative ROI commentary. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Roi Annotator

## Description
Enriches ledger transactions with qualitative ROI commentary. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "roi_annotator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "roi_annotator"`.
