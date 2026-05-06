---
skill: consumer_confidence_fetcher
category: public_data
description: Fetch the University of Michigan Consumer Sentiment Index from FRED (series UMCSENT). Returns latest value and 12-month trend.
tier: free
inputs: none
---

# Consumer Confidence Fetcher

## Description
Fetch the University of Michigan Consumer Sentiment Index from FRED (series UMCSENT). Returns latest value and 12-month trend. Requires FRED_API_KEY.

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
  "tool": "consumer_confidence_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "consumer_confidence_fetcher"`.
