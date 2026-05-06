---
skill: dispute_resolver
category: escrow
description: Determines auto, manual, or split dispute resolutions for escrow issues.
tier: free
inputs: dispute, resolution_type
---

# Dispute Resolver

## Description
Determines auto, manual, or split dispute resolutions for escrow issues.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dispute` | `object` | Yes |  |
| `resolution_type` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dispute_resolver",
  "arguments": {
    "dispute": {},
    "resolution_type": "<resolution_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dispute_resolver"`.
