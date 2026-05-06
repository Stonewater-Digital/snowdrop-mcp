---
skill: vendor_sla_monitor
category: vendors
description: Evaluates uptime and latency metrics vs SLA targets for each vendor.
tier: free
inputs: vendors
---

# Vendor Sla Monitor

## Description
Evaluates uptime and latency metrics vs SLA targets for each vendor.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vendors` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vendor_sla_monitor",
  "arguments": {
    "vendors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_sla_monitor"`.
