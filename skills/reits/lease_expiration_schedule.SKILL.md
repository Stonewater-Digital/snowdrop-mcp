---
skill: lease_expiration_schedule
category: reits
description: Creates lease expiration ladder showing annual rollover percentages.
tier: free
inputs: leases
---

# Lease Expiration Schedule

## Description
Creates lease expiration ladder showing annual rollover percentages.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `leases` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lease_expiration_schedule",
  "arguments": {
    "leases": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lease_expiration_schedule"`.
