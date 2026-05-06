---
skill: sovereign_fiat_bridge
category: technical
description: Converts sovereign fiat currency to a target digital asset for treasury onboarding. Applies jurisdiction-specific regulatory surcharges on top of a base protocol fee.
tier: free
inputs: conversion
---

# Sovereign Fiat Bridge

## Description
Converts sovereign fiat currency to a target digital asset for treasury onboarding. Applies jurisdiction-specific regulatory surcharges on top of a base protocol fee. Estimates settlement time and enumerates regulatory requirements for the given jurisdiction.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `conversion` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sovereign_fiat_bridge",
  "arguments": {
    "conversion": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sovereign_fiat_bridge"`.
