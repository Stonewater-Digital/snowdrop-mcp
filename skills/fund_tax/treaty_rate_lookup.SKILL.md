---
skill: treaty_rate_lookup
category: fund_tax
description: Returns statutory vs treaty withholding rates and article citations for major US treaties. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Treaty Rate Lookup

## Description
Returns statutory vs treaty withholding rates and article citations for major US treaties. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "treaty_rate_lookup",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "treaty_rate_lookup"`.
