---
skill: rwa_oracle_forestry_land_value_checker
category: crypto_rwa
description: Compares forestry land appraisal indexes with oracle quotes backing timber tokens.
tier: free
inputs: none
---

# Rwa Oracle Forestry Land Value Checker

## Description
Compares forestry land appraisal indexes with oracle quotes backing timber tokens.

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
  "tool": "rwa_oracle_forestry_land_value_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_forestry_land_value_checker"`.
