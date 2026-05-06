---
skill: rwa_real_estate_property_liens_status_monitor
category: crypto_rwa
description: Pulls lien registries to detect new encumbrances on token collateral.
tier: free
inputs: payload
---

# Rwa Real Estate Property Liens Status Monitor

## Description
Pulls lien registries to detect new encumbrances on token collateral.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_property_liens_status_monitor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_property_liens_status_monitor"`.
