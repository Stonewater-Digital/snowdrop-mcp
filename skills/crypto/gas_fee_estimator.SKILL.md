---
skill: gas_fee_estimator
category: crypto
description: Provides conservative fee estimates for TON and SOL transfers.
tier: free
inputs: chain, tx_size_bytes
---

# Gas Fee Estimator

## Description
Provides conservative fee estimates for TON and SOL transfers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `chain` | `string` | Yes |  |
| `tx_size_bytes` | `number` | Yes |  |
| `priority` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gas_fee_estimator",
  "arguments": {
    "chain": "<chain>",
    "tx_size_bytes": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gas_fee_estimator"`.
