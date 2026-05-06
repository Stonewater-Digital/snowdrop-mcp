---
skill: cap_floor_pricer
category: derivatives
description: Prices interest rate caps or floors using Black's model for each caplet/floorlet. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cap Floor Pricer

## Description
Prices interest rate caps or floors using Black's model for each caplet/floorlet. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cap_floor_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cap_floor_pricer"`.
