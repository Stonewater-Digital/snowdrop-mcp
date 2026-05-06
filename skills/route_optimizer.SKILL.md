---
skill: route_optimizer
category: root
description: Google Route Optimization API skill for fleet tour optimization, point-to-point directions, and distance matrix calculations. Supports real estate inspections, logistics planning, and multi-stop delivery sequencing.
tier: free
inputs: action
---

# Route Optimizer

## Description
Google Route Optimization API skill for fleet tour optimization, point-to-point directions, and distance matrix calculations. Supports real estate inspections, logistics planning, and multi-stop delivery sequencing.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | The routing operation to perform. |
| `origin` | `string` | No | Start address or 'lat,lng' string. |
| `destination` | `string` | No | End address or 'lat,lng' string. |
| `waypoints` | `array` | No | Intermediate stops for directions (max 25). |
| `vehicles` | `array` | No | Fleet vehicles with start_location, end_location, cost_per_hour. |
| `shipments` | `array` | No | Pickup/delivery tasks with arrival_location and load_demands. |
| `departure_time` | `string` | No | ISO8601 departure time for traffic-aware routing. |
| `mode` | `string` | No | Travel mode for directions and distance_matrix. |
| `avoid` | `array` | No | Route features to avoid: tolls, highways, ferries. |
| `project_id` | `string` | No | GCP project ID. Falls back to GOOGLE_PROJECT_ID env var. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "route_optimizer",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "route_optimizer"`.
