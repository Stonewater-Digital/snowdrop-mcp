---
skill: precious_metals_lease_rate
category: commodities
description: Derives the implied precious metals lease rate from spot, forward, and USD interest rate inputs. Uses the GOFO (Gold Forward Offered Rate) identity: Lease Rate = USD Rate − GOFO, where GOFO = annualized forward premium.
tier: free
inputs: spot_price, forward_price, tenor_days, usd_rate_pct
---

# Precious Metals Lease Rate

## Description
Derives the implied precious metals lease rate from spot, forward, and USD interest rate inputs. Uses the GOFO (Gold Forward Offered Rate) identity: Lease Rate = USD Rate − GOFO, where GOFO = annualized forward premium.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes | Spot price of the metal in USD/oz (must be > 0). |
| `forward_price` | `number` | Yes | Forward price of the metal in USD/oz for the given tenor (must be > 0). |
| `tenor_days` | `number` | Yes | Tenor of the forward contract in calendar days (must be > 0). |
| `usd_rate_pct` | `number` | Yes | Annualized USD LIBOR/SOFR interest rate as % for the same tenor. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "precious_metals_lease_rate",
  "arguments": {
    "spot_price": 0,
    "forward_price": 0,
    "tenor_days": 0,
    "usd_rate_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "precious_metals_lease_rate"`.
