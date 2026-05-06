---
skill: rwa_real_estate_property_liens_status_monitor
category: crypto_rwa
description: Pulls lien registries to detect new encumbrances on token collateral.
tier: free
inputs: none
---

# Rwa Real Estate Property Liens Status Monitor

## Description
Pulls lien registries to detect new encumbrances on token collateral.

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
  "tool": "rwa_real_estate_property_liens_status_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_property_liens_status_monitor"`.
