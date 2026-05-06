---
skill: us_state_co_fund_tax
category: fund_tax
description: Computes Colorado income tax, elective entity-level tax, and nonresident withholding obligations referencing Colo. Rev.
tier: premium
inputs: none
---

# Us State Co Fund Tax

## Description
Computes Colorado income tax, elective entity-level tax, and nonresident withholding obligations referencing Colo. Rev. Stat. §§39-22-104 and 39-22-601. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_co_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_co_fund_tax"`.
