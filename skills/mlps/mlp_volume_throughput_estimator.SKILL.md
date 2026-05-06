---
skill: mlp_volume_throughput_estimator
category: mlps
description: Measures asset utilization and tariff revenue for MLP pipeline systems. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Volume Throughput Estimator

## Description
Measures asset utilization and tariff revenue for MLP pipeline systems. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_volume_throughput_estimator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_volume_throughput_estimator"`.
