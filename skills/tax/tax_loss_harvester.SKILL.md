---
skill: tax_loss_harvester
category: tax
description: Ranks positions by after-tax savings potential with wash sale warnings.
tier: free
inputs: positions
---

# Tax Loss Harvester

## Description
Ranks positions by after-tax savings potential with wash sale warnings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `short_term_rate` | `number` | No |  |
| `long_term_rate` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tax_loss_harvester",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_loss_harvester"`.
