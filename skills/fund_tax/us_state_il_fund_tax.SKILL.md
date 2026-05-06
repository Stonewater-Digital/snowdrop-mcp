---
skill: us_state_il_fund_tax
category: fund_tax
description: Models Illinois individual income rate, replacement tax, and the entity-level election mandated by Public Act 102-0658. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Il Fund Tax

## Description
Models Illinois individual income rate, replacement tax, and the entity-level election mandated by Public Act 102-0658. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_il_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_il_fund_tax"`.
