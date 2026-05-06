---
skill: federal_funds_rate_fetcher
category: public_data
description: Fetch the effective Federal Funds Rate from FRED (series FEDFUNDS). Returns latest rate and recent history.
tier: free
inputs: none
---

# Federal Funds Rate Fetcher

## Description
Fetch the effective Federal Funds Rate from FRED (series FEDFUNDS). Returns latest rate and recent history. Requires FRED_API_KEY.

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
  "tool": "federal_funds_rate_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "federal_funds_rate_fetcher"`.
