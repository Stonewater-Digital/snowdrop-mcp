---
skill: rwa_oracle_block_timestamp_gapper
category: crypto_rwa
description: Measures block timestamp gaps affecting TWAP-driven oracle updates.
tier: free
inputs: none
---

# Rwa Oracle Block Timestamp Gapper

## Description
Measures block timestamp gaps affecting TWAP-driven oracle updates.

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
  "tool": "rwa_oracle_block_timestamp_gapper",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_block_timestamp_gapper"`.
