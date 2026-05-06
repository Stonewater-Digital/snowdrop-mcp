---
skill: rwa_private_credit_nav_facility_limit_monitor
category: crypto_rwa
description: Checks NAV facility utilization versus limits before approving new draws.
tier: free
inputs: none
---

# Rwa Private Credit Nav Facility Limit Monitor

## Description
Checks NAV facility utilization versus limits before approving new draws.

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
  "tool": "rwa_private_credit_nav_facility_limit_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_private_credit_nav_facility_limit_monitor"`.
