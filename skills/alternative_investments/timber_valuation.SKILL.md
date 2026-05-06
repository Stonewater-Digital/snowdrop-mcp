---
skill: timber_valuation
category: alternative_investments
description: Applies Faustmann formula to timber growth and stumpage pricing to compute NPV and optimal rotation age. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Timber Valuation

## Description
Applies Faustmann formula to timber growth and stumpage pricing to compute NPV and optimal rotation age. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "timber_valuation",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "timber_valuation"`.
