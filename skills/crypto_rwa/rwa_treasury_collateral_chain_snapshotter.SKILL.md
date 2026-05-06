---
skill: rwa_treasury_collateral_chain_snapshotter
category: crypto_rwa
description: Builds snapshots of collateral pledges to avoid double counting the same bills.
tier: free
inputs: none
---

# Rwa Treasury Collateral Chain Snapshotter

## Description
Builds snapshots of collateral pledges to avoid double counting the same bills.

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
  "tool": "rwa_treasury_collateral_chain_snapshotter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_collateral_chain_snapshotter"`.
