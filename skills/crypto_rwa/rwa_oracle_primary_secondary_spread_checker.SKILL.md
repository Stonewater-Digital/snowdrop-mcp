---
skill: rwa_oracle_primary_secondary_spread_checker
category: crypto_rwa
description: Compares primary issuance prices with secondary token trading to spot gaps.
tier: free
inputs: none
---

# Rwa Oracle Primary Secondary Spread Checker

## Description
Compares primary issuance prices with secondary token trading to spot gaps.

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
  "tool": "rwa_oracle_primary_secondary_spread_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_primary_secondary_spread_checker"`.
