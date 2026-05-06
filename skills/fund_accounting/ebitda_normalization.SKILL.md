---
skill: ebitda_normalization
category: fund_accounting
description: Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Ebitda Normalization

## Description
Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "ebitda_normalization",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ebitda_normalization"`.
