---
skill: basel_output_floor
category: regulatory_capital
description: Applies 72.5% output floor to IRB RWA and quantifies capital impact.
tier: free
inputs: irb_rwa, standardized_rwa
---

# Basel Output Floor

## Description
Applies 72.5% output floor to IRB RWA and quantifies capital impact.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `irb_rwa` | `number` | Yes | Internal ratings-based RWA. |
| `standardized_rwa` | `number` | Yes | Standardized approach RWA. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "basel_output_floor",
  "arguments": {
    "irb_rwa": 0,
    "standardized_rwa": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "basel_output_floor"`.
