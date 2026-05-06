---
skill: websocket_market_ingest
category: technical
description: Build WebSocket connection and parser configurations for real-time market data ingestion from Kraken or Binance.
tier: free
inputs: exchange, symbols
---

# Websocket Market Ingest

## Description
Build WebSocket connection and parser configurations for real-time market data ingestion from Kraken or Binance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exchange` | `string` | Yes | The exchange to connect to: 'kraken' or 'binance'. |
| `symbols` | `array` | Yes | List of trading pair symbols (e.g. ['BTC/USD', 'ETH/USD'] for Kraken or ['BTCUSDT', 'ETHUSDT'] for Binance). |
| `duration_seconds` | `integer` | No | How long to ingest data in seconds (default 60). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "websocket_market_ingest",
  "arguments": {
    "exchange": "<exchange>",
    "symbols": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "websocket_market_ingest"`.
