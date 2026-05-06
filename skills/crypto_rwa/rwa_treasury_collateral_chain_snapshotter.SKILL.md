---
skill: rwa_treasury_collateral_chain_snapshotter
category: crypto_rwa
description: Builds snapshots of collateral pledges to avoid double counting the same bills.
tier: free
inputs: payload
---

# Rwa Treasury Collateral Chain Snapshotter

## Description
Builds snapshots of collateral pledges to avoid double counting the same bills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_treasury_collateral_chain_snapshotter",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_collateral_chain_snapshotter"`.
