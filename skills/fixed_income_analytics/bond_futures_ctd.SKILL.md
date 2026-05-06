---
skill: bond_futures_ctd
category: fixed_income_analytics
description: Evaluates conversion-factor adjusted invoice price, carry, and implied repo rate to identify the CTD bond per CME Treasury delivery rules. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Bond Futures Ctd

## Description
Evaluates conversion-factor adjusted invoice price, carry, and implied repo rate to identify the CTD bond per CME Treasury delivery rules. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "bond_futures_ctd",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_futures_ctd"`.
