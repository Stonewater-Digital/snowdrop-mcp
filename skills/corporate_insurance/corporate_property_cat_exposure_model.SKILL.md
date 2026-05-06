---
skill: corporate_property_cat_exposure_model
category: corporate_insurance
description: Summarizes property exposure by peril zone and cat return periods.
tier: free
inputs: locations
---

# Corporate Property Cat Exposure Model

## Description
Summarizes property exposure by peril zone and cat return periods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `locations` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "corporate_property_cat_exposure_model",
  "arguments": {
    "locations": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "corporate_property_cat_exposure_model"`.
