---
skill: yield_curve_fetcher
category: public_data
description: Fetch the US Treasury yield curve across multiple maturities (1M to 30Y) from the Treasury Fiscal Data API. Includes inversion detection.
tier: free
inputs: none
---

# Yield Curve Fetcher

## Description
Fetch the US Treasury yield curve across multiple maturities (1M to 30Y) from the Treasury Fiscal Data API. Includes inversion detection. No API key required.

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
  "tool": "yield_curve_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "yield_curve_fetcher"`.
