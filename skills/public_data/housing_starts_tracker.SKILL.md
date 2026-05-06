---
skill: housing_starts_tracker
category: public_data
description: Track US housing starts from FRED (series HOUST). Returns latest value and year-over-year change.
tier: free
inputs: none
---

# Housing Starts Tracker

## Description
Track US housing starts from FRED (series HOUST). Returns latest value and year-over-year change. Requires FRED_API_KEY.

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
  "tool": "housing_starts_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "housing_starts_tracker"`.
