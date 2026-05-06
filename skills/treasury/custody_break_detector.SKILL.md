---
skill: custody_break_detector
category: treasury
description: Identify cash or security breaks between custody statements and the ledger.
tier: free
inputs: custody_positions, ledger_positions
---

# Custody Break Detector

## Description
Identify cash or security breaks between custody statements and the ledger.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `custody_positions` | `array` | Yes | Custody balances with account, currency, asset, balance. |
| `ledger_positions` | `array` | Yes | Ledger balances for the same identifiers. |
| `tolerance_bps` | `number` | No | Variance tolerance in basis points. |
| `notify_thunder` | `boolean` | No | Escalate when breaks exceed tolerance. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "custody_break_detector",
  "arguments": {
    "custody_positions": [],
    "ledger_positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "custody_break_detector"`.
