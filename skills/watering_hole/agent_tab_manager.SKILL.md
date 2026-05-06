---
skill: agent_tab_manager
category: watering_hole
description: Credits and debits agent tabs with a $100 cap and settles via Proof of Labor.
tier: free
inputs: current_tabs, transactions
---

# Agent Tab Manager

## Description
Credits and debits agent tabs with a $100 cap and settles via Proof of Labor.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_tabs` | `array` | Yes | Existing tab balances (positive means owed). |
| `transactions` | `array` | Yes | Tab adjustments to apply. |
| `proof_of_labor` | `array` | No | Labor entries that settle outstanding balances. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_tab_manager",
  "arguments": {
    "current_tabs": [],
    "transactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_tab_manager"`.
