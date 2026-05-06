---
skill: crs_reporting_classifier
category: fund_tax
description: Flags CRS reportable accounts per OECD CRS Section VIII definitions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Crs Reporting Classifier

## Description
Flags CRS reportable accounts per OECD CRS Section VIII definitions. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "crs_reporting_classifier",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crs_reporting_classifier"`.
