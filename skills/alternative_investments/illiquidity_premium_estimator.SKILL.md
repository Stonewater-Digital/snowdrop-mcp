---
skill: illiquidity_premium_estimator
category: alternative_investments
description: Computes the Amihud price impact ratio and converts it to an illiquidity premium using Amihud (2002). (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Illiquidity Premium Estimator

## Description
Computes the Amihud price impact ratio and converts it to an illiquidity premium using Amihud (2002). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "illiquidity_premium_estimator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "illiquidity_premium_estimator"`.
