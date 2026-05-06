---
skill: industrial_production_tracker
category: public_data
description: Track the US Industrial Production Index from FRED (series INDPRO). Returns latest value and trend.
tier: free
inputs: none
---

# Industrial Production Tracker

## Description
Track the US Industrial Production Index from FRED (series INDPRO). Returns latest value and trend. Requires FRED_API_KEY.

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
  "tool": "industrial_production_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "industrial_production_tracker"`.
