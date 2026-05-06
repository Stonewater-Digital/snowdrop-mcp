---
skill: intl_sa_fund_tax
category: fund_tax
description: Evaluates Saudi withholding and the 20% income tax plus 2.5% Zakat overlay for onshore operations. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Sa Fund Tax

## Description
Evaluates Saudi withholding and the 20% income tax plus 2.5% Zakat overlay for onshore operations. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_sa_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_sa_fund_tax"`.
