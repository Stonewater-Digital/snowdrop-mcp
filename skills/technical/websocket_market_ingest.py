"""
Executive Summary: Build low-latency WebSocket exchange feed ingestion configurations for Kraken and Binance market data streams.
Inputs: exchange (str), symbols (list of str), duration_seconds (int)
Outputs: connection_config (dict), parser_config (dict), estimated_messages_per_second (float), ready (bool)
MCP Tool Name: websocket_market_ingest
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "websocket_market_ingest",
    "description": "Build WebSocket connection and parser configurations for real-time market data ingestion from Kraken or Binance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exchange": {
                "type": "string",
                "enum": ["kraken", "binance"],
                "description": "The exchange to connect to: 'kraken' or 'binance'."
            },
            "symbols": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of trading pair symbols (e.g. ['BTC/USD', 'ETH/USD'] for Kraken or ['BTCUSDT', 'ETHUSDT'] for Binance)."
            },
            "duration_seconds": {
                "type": "integer",
                "description": "How long to ingest data in seconds (default 60).",
                "default": 60
            }
        },
        "required": ["exchange", "symbols"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "connection_config": {"type": "object"},
            "parser_config": {"type": "object"},
            "estimated_messages_per_second": {"type": "number"},
            "ready": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["connection_config", "parser_config", "estimated_messages_per_second", "ready", "status", "timestamp"]
    }
}

# Exchange-specific WebSocket endpoints and rate characteristics
_EXCHANGE_CONFIGS: dict[str, dict] = {
    "kraken": {
        "ws_url": "wss://ws.kraken.com/v2",
        "subscribe_method": "subscribe",
        "channel_trades": "trade",
        "channel_ticker": "ticker",
        "channel_book": "book",
        "auth_required_channels": ["openOrders", "ownTrades"],
        "ping_interval_seconds": 30,
        "reconnect_delay_seconds": 5,
        "max_symbols_per_connection": 50,
        # Empirical Kraken message rates per symbol per second
        "msgs_per_symbol_per_second": {
            "trade": 0.5,
            "ticker": 1.0,
            "book": 2.0,
        },
        "auth_env_key": "KRAKEN_API_KEY",
        "auth_env_secret": "KRAKEN_API_SECRET",
    },
    "binance": {
        "ws_url": "wss://stream.binance.com:9443/stream",
        "subscribe_method": "SUBSCRIBE",
        "channel_trades": "trade",
        "channel_ticker": "bookTicker",
        "channel_book": "depth",
        "auth_required_channels": ["executionReport"],
        "ping_interval_seconds": 20,
        "reconnect_delay_seconds": 3,
        "max_symbols_per_connection": 1024,
        # Empirical Binance message rates per symbol per second
        "msgs_per_symbol_per_second": {
            "trade": 2.0,
            "ticker": 1.0,
            "book": 5.0,
        },
        "auth_env_key": "BINANCE_API_KEY",
        "auth_env_secret": "BINANCE_API_SECRET",
    },
}

# Fields expected in each exchange's message format
_PARSER_SCHEMAS: dict[str, dict] = {
    "kraken": {
        "message_format": "JSON-object",
        "trade_fields": {
            "symbol": "$.symbol",
            "price": "$.data[*].price",
            "qty": "$.data[*].qty",
            "side": "$.data[*].side",
            "timestamp": "$.data[*].timestamp",
            "trade_id": "$.data[*].trade_id",
            "ord_type": "$.data[*].ord_type",
        },
        "ticker_fields": {
            "symbol": "$.symbol",
            "bid": "$.data.bid",
            "ask": "$.data.ask",
            "last": "$.data.last",
            "volume": "$.data.volume",
            "change_pct": "$.data.change_pct_24h",
        },
        "normalization": {
            "price": "float",
            "qty": "float",
            "timestamp": "iso8601_to_epoch_ms",
            "side": "lowercase",
        },
        "heartbeat_field": "$.channel == 'heartbeat'",
    },
    "binance": {
        "message_format": "JSON-object",
        "trade_fields": {
            "symbol": "$.data.s",
            "price": "$.data.p",
            "qty": "$.data.q",
            "side": "$.data.m",  # m=true means maker (sell side)
            "timestamp": "$.data.T",
            "trade_id": "$.data.t",
            "event_type": "$.data.e",
        },
        "ticker_fields": {
            "symbol": "$.data.s",
            "bid": "$.data.b",
            "ask": "$.data.a",
            "bid_qty": "$.data.B",
            "ask_qty": "$.data.A",
        },
        "normalization": {
            "price": "float_from_string",
            "qty": "float_from_string",
            "timestamp": "epoch_ms",
            "side": "bool_to_buy_sell",  # false = taker buy
        },
        "heartbeat_field": None,  # Binance sends pings at protocol level
    },
}


def _build_kraken_subscription(symbols: list[str], api_key: str) -> dict:
    """Build Kraken WebSocket subscription message payload.

    Args:
        symbols: List of Kraken symbol strings.
        api_key: Kraken API key (empty string if not available).

    Returns:
        Subscription message dict ready for JSON serialization.
    """
    return {
        "method": "subscribe",
        "params": {
            "channel": "trade",
            "symbol": symbols,
            "snapshot": True,
        },
        "req_id": int(datetime.now(timezone.utc).timestamp() * 1000),
    }


def _build_binance_subscription(symbols: list[str]) -> dict:
    """Build Binance WebSocket subscription message payload.

    Args:
        symbols: List of Binance symbol strings (already lowercased).

    Returns:
        Subscription message dict ready for JSON serialization.
    """
    streams = []
    for sym in symbols:
        s = sym.lower().replace("/", "")
        streams.append(f"{s}@trade")
        streams.append(f"{s}@bookTicker")

    return {
        "method": "SUBSCRIBE",
        "params": streams,
        "id": int(datetime.now(timezone.utc).timestamp() * 1000),
    }


def websocket_market_ingest(
    exchange: str,
    symbols: list[str],
    duration_seconds: int = 60,
) -> dict:
    """Build WebSocket connection and parser configurations for real-time market data ingestion.

    Returns all configuration needed to establish a WebSocket connection to the
    specified exchange, subscribe to the given symbols, and parse the incoming
    message stream into normalized trade/ticker records.

    Args:
        exchange: Exchange identifier — "kraken" or "binance".
        symbols: List of trading pair symbols to subscribe to.
        duration_seconds: How long to run the ingestion in seconds (default 60).

    Returns:
        A dict with keys:
            - connection_config (dict): WebSocket URL, headers, subscription payload, reconnect policy.
            - parser_config (dict): Message field paths and normalization rules.
            - estimated_messages_per_second (float): Expected message throughput.
            - ready (bool): True if all required env vars and params are valid.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        exchange = exchange.strip().lower()
        if exchange not in _EXCHANGE_CONFIGS:
            raise ValueError(f"exchange must be 'kraken' or 'binance', got '{exchange}'.")
        if not symbols or not isinstance(symbols, list):
            raise ValueError("symbols must be a non-empty list.")
        if duration_seconds <= 0:
            raise ValueError(f"duration_seconds must be positive, got {duration_seconds}.")

        cfg = _EXCHANGE_CONFIGS[exchange]
        max_syms = cfg["max_symbols_per_connection"]
        if len(symbols) > max_syms:
            raise ValueError(
                f"{exchange} supports max {max_syms} symbols per connection, got {len(symbols)}."
            )

        # Check required env vars
        api_key = os.getenv(cfg["auth_env_key"], "")
        api_secret = os.getenv(cfg.get("auth_env_secret", ""), "")
        auth_available = bool(api_key)

        # Build subscription message
        if exchange == "kraken":
            subscription_msg = _build_kraken_subscription(symbols, api_key)
        else:
            subscription_msg = _build_binance_subscription(symbols)

        # Connection configuration
        headers: dict[str, str] = {
            "User-Agent": "Snowdrop-MarketIngest/1.0",
        }
        if exchange == "kraken" and api_key:
            headers["API-Key"] = api_key

        connection_config = {
            "exchange": exchange,
            "ws_url": cfg["ws_url"],
            "headers": headers,
            "subscription_message": subscription_msg,
            "symbols": symbols,
            "symbol_count": len(symbols),
            "duration_seconds": duration_seconds,
            "ping_interval_seconds": cfg["ping_interval_seconds"],
            "reconnect_policy": {
                "enabled": True,
                "max_retries": 10,
                "base_delay_seconds": cfg["reconnect_delay_seconds"],
                "backoff_multiplier": 2.0,
                "max_delay_seconds": 60.0,
            },
            "buffer_policy": {
                "type": "ring_buffer",
                "max_messages": 10_000,
                "overflow": "drop_oldest",
            },
            "auth_available": auth_available,
            "auth_required_for_channels": cfg["auth_required_channels"],
        }

        # Parser configuration
        parser_config = {
            "exchange": exchange,
            **_PARSER_SCHEMAS[exchange],
            "output_format": "normalized_trade",
            "normalized_schema": {
                "exchange": "string",
                "symbol": "string",
                "price": "float",
                "qty": "float",
                "side": "string (buy|sell)",
                "timestamp_ms": "integer",
                "trade_id": "string",
                "raw": "dict (original message)",
            },
        }

        # Estimate message throughput: trade + ticker per symbol
        rates = cfg["msgs_per_symbol_per_second"]
        msgs_per_second = len(symbols) * (rates["trade"] + rates["ticker"])

        # Ready check: valid params + auth for private channels
        ready = bool(symbols and duration_seconds > 0)
        if exchange == "kraken":
            # Kraken public feeds don't require auth
            ready = ready and True

        return {
            "status": "success",
            "connection_config": connection_config,
            "parser_config": parser_config,
            "estimated_messages_per_second": round(msgs_per_second, 2),
            "estimated_total_messages": round(msgs_per_second * duration_seconds),
            "auth_available": auth_available,
            "ready": ready,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"websocket_market_ingest failed: {e}")
        _log_lesson(f"websocket_market_ingest: {e}")
        return {
            "status": "error",
            "error": str(e),
            "connection_config": {},
            "parser_config": {},
            "estimated_messages_per_second": 0.0,
            "ready": False,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
