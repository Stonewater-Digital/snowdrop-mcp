---
skill: rwa_real_estate_deed_forgery_scanner
category: crypto_rwa
description: Analyzes notarized deed uploads for signature anomalies and tamper patterns before minting tokens.
tier: free
inputs: none
---

# Rwa Real Estate Deed Forgery Scanner

## Description
Analyzes notarized deed uploads for signature anomalies and tamper patterns before minting tokens.

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
  "tool": "rwa_real_estate_deed_forgery_scanner",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_deed_forgery_scanner"`.
