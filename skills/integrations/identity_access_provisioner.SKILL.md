---
skill: identity_access_provisioner
category: integrations
description: Generate provisioning instructions for identity requests with entitlements and expiry validation.
tier: free
inputs: requests
---

# Identity Access Provisioner

## Description
Generate provisioning instructions for identity requests with entitlements and expiry validation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `requests` | `array` | Yes | Requests with user, roles, system, justification, and requested_until fields. |
| `role_matrix` | `object` | No | Mapping of role -> entitlements/groups to assign. |
| `default_expiry_days` | `integer` | No | Fallback expiry window when not supplied on the request. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "identity_access_provisioner",
  "arguments": {
    "requests": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "identity_access_provisioner"`.
