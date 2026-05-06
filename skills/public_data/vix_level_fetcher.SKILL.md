---
skill: vix_level_fetcher
category: public_data
description: Fetch the CBOE Volatility Index (VIX) from FRED (series VIXCLS). Returns latest level with interpretation.
tier: free
inputs: none
---

# Vix Level Fetcher

## Description
Fetch the CBOE Volatility Index (VIX) from FRED (series VIXCLS). Returns latest level with interpretation. Requires FRED_API_KEY.

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
  "tool": "vix_level_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vix_level_fetcher"`.
