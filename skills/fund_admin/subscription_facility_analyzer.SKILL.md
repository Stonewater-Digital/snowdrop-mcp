---
skill: subscription_facility_analyzer
category: fund_admin
description: Evaluates subscription credit facility utilization, annualized interest cost, unused fee drag, and NAV impact. Subscription lines are backed by LP commitments.
tier: premium
inputs: none
---

# Subscription Facility Analyzer

## Description
Evaluates subscription credit facility utilization, annualized interest cost, unused fee drag, and NAV impact. Subscription lines are backed by LP commitments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "subscription_facility_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "subscription_facility_analyzer"`.
