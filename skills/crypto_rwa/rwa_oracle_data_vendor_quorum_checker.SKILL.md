---
skill: rwa_oracle_data_vendor_quorum_checker
category: crypto_rwa
description: Ensures quorum logic across multiple vendors is functioning and weighted correctly.
tier: free
inputs: none
---

# Rwa Oracle Data Vendor Quorum Checker

## Description
Ensures quorum logic across multiple vendors is functioning and weighted correctly.

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
  "tool": "rwa_oracle_data_vendor_quorum_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_data_vendor_quorum_checker"`.
