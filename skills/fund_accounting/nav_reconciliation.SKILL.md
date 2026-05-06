---
skill: nav_reconciliation
category: fund_accounting
description: Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Nav Reconciliation

## Description
Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "nav_reconciliation",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nav_reconciliation"`.
