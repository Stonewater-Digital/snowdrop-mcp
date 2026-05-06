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
| `vendors` | `array` | Yes | List of vendor objects, each with `name`, `uptime_pct` (float 0–100), `latency_ms` (float), and `sla_targets` (object with `min_uptime_pct` and `max_latency_ms`). |

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
    "vendors": [
      {
        "name": "OpenRouter",
        "uptime_pct": 99.1,
        "latency_ms": 320,
        "sla_targets": {"min_uptime_pct": 99.5, "max_latency_ms": 500}
      }
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_sla_monitor"`.
