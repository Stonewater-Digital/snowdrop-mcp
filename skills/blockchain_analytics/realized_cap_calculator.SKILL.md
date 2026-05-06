---
skill: realized_cap_calculator
category: blockchain_analytics
description: Computes realized capitalization from UTXO-style inputs and infers unrealized profit and supply composition.
tier: free
inputs: utxo_set
---

# Realized Cap Calculator

## Description
Computes realized capitalization from UTXO-style inputs and infers unrealized profit and supply composition.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `utxo_set` | `array` | Yes | List of unspent outputs each containing amount and price_at_creation fields. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "realized_cap_calculator",
  "arguments": {
    "utxo_set": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "realized_cap_calculator"`.
