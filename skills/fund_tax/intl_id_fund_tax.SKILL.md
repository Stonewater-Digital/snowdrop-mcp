---
skill: intl_id_fund_tax
category: fund_tax
description: Captures Indonesian withholding (including the 0.1% share transfer tax) and the 22% corporate income tax on local operations. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Id Fund Tax

## Description
Captures Indonesian withholding (including the 0.1% share transfer tax) and the 22% corporate income tax on local operations. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_id_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_id_fund_tax"`.
