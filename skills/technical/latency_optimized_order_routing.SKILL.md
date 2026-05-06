---
skill: latency_optimized_order_routing
category: technical
description: Selects the optimal server route for a trade order by ranking available exchange server locations by latency and filtering out unreliable routes (reliability < 99%). Returns the winning route, ranked alternatives, and estimated execution time advantage over the median route.
tier: premium
inputs: none
---

# Latency Optimized Order Routing

## Description
Selects the optimal server route for a trade order by ranking available exchange server locations by latency and filtering out unreliable routes (reliability < 99%). Returns the winning route, ranked alternatives, and estimated execution time advantage over the median route. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "latency_optimized_order_routing",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "latency_optimized_order_routing"`.
