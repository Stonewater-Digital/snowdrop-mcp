---
skill: capital_call_fx_optimizer
category: fund_accounting
description: Allocates multi-currency balances to satisfy a capital call with minimal FX drag. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Capital Call Fx Optimizer

## Description
Allocates multi-currency balances to satisfy a capital call with minimal FX drag. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "capital_call_fx_optimizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_call_fx_optimizer"`.
