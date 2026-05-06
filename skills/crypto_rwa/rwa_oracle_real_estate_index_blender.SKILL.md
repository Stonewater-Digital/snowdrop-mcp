---
skill: rwa_oracle_real_estate_index_blender
category: crypto_rwa
description: Blends Case-Shiller and proprietary comps to smooth real-estate NAV ticks feeding tokens.
tier: free
inputs: none
---

# Rwa Oracle Real Estate Index Blender

## Description
Blends Case-Shiller and proprietary comps to smooth real-estate NAV ticks feeding tokens.

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
  "tool": "rwa_oracle_real_estate_index_blender",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_real_estate_index_blender"`.
