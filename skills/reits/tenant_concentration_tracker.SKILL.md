---
skill: tenant_concentration_tracker
category: reits
description: Flags top tenant exposure versus single-tenant and top-10 limits.
tier: free
inputs: tenants
---

# Tenant Concentration Tracker

## Description
Flags top tenant exposure versus single-tenant and top-10 limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tenants` | `array` | Yes |  |
| `single_tenant_limit_pct` | `number` | No |  |
| `top_ten_limit_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tenant_concentration_tracker",
  "arguments": {
    "tenants": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tenant_concentration_tracker"`.
