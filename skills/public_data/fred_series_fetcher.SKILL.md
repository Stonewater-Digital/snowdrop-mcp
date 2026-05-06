---
skill: fred_series_fetcher
category: public_data
description: Fetch economic data series observations from the FRED API by series ID (e.g., GDP, UNRATE, CPIAUCSL). Requires FRED_API_KEY environment variable.
tier: free
inputs: series_id
---

# Fred Series Fetcher

## Description
Fetch economic data series observations from the FRED API by series ID (e.g., GDP, UNRATE, CPIAUCSL). Requires FRED_API_KEY environment variable.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `series_id` | `string` | Yes | FRED series ID (e.g., 'GDP', 'UNRATE', 'CPIAUCSL'). |
| `observation_start` | `string` | No | Start date in YYYY-MM-DD format. Optional. |
| `observation_end` | `string` | No | End date in YYYY-MM-DD format. Optional. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fred_series_fetcher",
  "arguments": {
    "series_id": "<series_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fred_series_fetcher"`.
