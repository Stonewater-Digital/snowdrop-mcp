"""
Market Cap Tracker - Real-time cryptocurrency market capitalization tracker
MCP Skill for Snowdrop
Author: Claw-Agent
"""

from __future__ import annotations
import os
import logging
import requests
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "market_cap_tracker",
    "description": "Track real-time cryptocurrency market capitalization, price, and trading volume for top cryptocurrencies. Supports ranking, filtering, and historical comparison.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Cryptocurrency symbol (e.g., 'BTC', 'ETH', 'SOL'). Use 'TOP' for top 10 list."
            },
            "currency": {
                "type": "string",
                "description": "Quote currency for price display (default: 'USD')",
                "default": "USD",
                "enum": ["USD", "EUR", "CNY", "BTC", "ETH"]
            },
            "include_market_data": {
                "type": "boolean",
                "description": "Include detailed market data (volume, supply, dominance)",
                "default": True
            }
        },
        "required": ["symbol"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "data": {"type": "object"},
            "rank": {"type": "integer"},
            "timestamp": {"type": "string"},
            "status": {"type": "string"}
        },
        "required": ["data", "status", "timestamp"]
    }
}

# CoinGecko API configuration
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINGECKO_PRO_BASE = "https://pro-api.coingecko.com/api/v3"

# Top cryptocurrency mappings (symbol -> CoinGecko ID)
CRYPTO_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "TRX": "tron",
    "AVAX": "avalanche-2",
    "LINK": "chainlink",
    "TON": "the-open-network",
    "DOT": "polkadot",
    "MATIC": "matic-network",
    "SHIB": "shiba-inu",
    "LTC": "litecoin",
    "UNI": "uniswap",
    "ATOM": "cosmos",
    "XLM": "stellar",
    "OKB": "okb",
    "FIL": "filecoin",
}


def _get_api_base() -> str:
    """Determine which CoinGecko API endpoint to use."""
    pro_key = os.getenv("COINGECKO_PRO_API_KEY")
    if pro_key:
        return COINGECKO_PRO_BASE
    return COINGECKO_API_BASE


def _get_headers() -> dict[str, str]:
    """Build request headers including API key if available."""
    headers = {
        "Accept": "application/json",
        "User-Agent": "Snowdrop-MarketCapTracker/1.0"
    }
    pro_key = os.getenv("COINGECKO_PRO_API_KEY")
    if pro_key:
        headers["x-cg-pro-api-key"] = pro_key
    return headers


def _format_currency(value: float, currency: str) -> str:
    """Format currency value with appropriate symbol."""
    symbols = {
        "USD": "$",
        "EUR": "€",
        "CNY": "¥",
        "BTC": "₿",
        "ETH": "Ξ"
    }
    symbol = symbols.get(currency, "$")
    
    if value >= 1_000_000_000_000:
        return f"{symbol}{value/1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:
        return f"{symbol}{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{symbol}{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{symbol}{value/1_000:.2f}K"
    else:
        return f"{symbol}{value:,.2f}"


def _format_percentage(value: float) -> str:
    """Format percentage change with sign and color indicator."""
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def _fetch_top_coins(vs_currency: str = "usd", limit: int = 10) -> list[dict]:
    """Fetch top cryptocurrencies by market cap."""
    base_url = _get_api_base()
    headers = _get_headers()
    
    url = f"{base_url}/coins/markets"
    params = {
        "vs_currency": vs_currency.lower(),
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h,7d"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch top coins: {e}")
        raise


def _fetch_coin_data(coin_id: str, vs_currency: str = "usd") -> dict:
    """Fetch detailed data for a specific coin."""
    base_url = _get_api_base()
    headers = _get_headers()
    
    url = f"{base_url}/coins/{coin_id}"
    params = {
        "localization": False,
        "tickers": False,
        "market_data": True,
        "community_data": False,
        "developer_data": False,
        "sparkline": False
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch coin data for {coin_id}: {e}")
        raise


def market_cap_tracker(
    symbol: str,
    currency: str = "USD",
    include_market_data: bool = True
) -> dict:
    """
    Track cryptocurrency market capitalization and price data.
    
    Provides real-time market cap, price, volume, and ranking information
    for cryptocurrencies. Supports both individual coin lookup and top 10 lists.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH', 'SOL') or 'TOP' for top 10
        currency: Quote currency for prices (USD, EUR, CNY, BTC, ETH)
        include_market_data: Whether to include detailed market metrics
    
    Returns:
        Dict containing market data, rank, and metadata
    """
    try:
        symbol_upper = symbol.upper().strip()
        vs_currency = currency.lower()
        
        if symbol_upper == "TOP":
            # Fetch top 10 cryptocurrencies
            coins = _fetch_top_coins(vs_currency, limit=10)
            
            top_list = []
            for coin in coins:
                item = {
                    "rank": coin.get("market_cap_rank", 0),
                    "symbol": coin.get("symbol", "").upper(),
                    "name": coin.get("name", ""),
                    "price": coin.get("current_price", 0),
                    "price_formatted": _format_currency(coin.get("current_price", 0), currency),
                    "market_cap": coin.get("market_cap", 0),
                    "market_cap_formatted": _format_currency(coin.get("market_cap", 0), currency),
                }
                
                if include_market_data:
                    price_change_24h = coin.get("price_change_percentage_24h", 0) or 0
                    price_change_7d = coin.get("price_change_percentage_7d_in_currency", 0) or 0
                    
                    item.update({
                        "volume_24h": coin.get("total_volume", 0),
                        "volume_formatted": _format_currency(coin.get("total_volume", 0), currency),
                        "circulating_supply": coin.get("circulating_supply", 0),
                        "price_change_24h": price_change_24h,
                        "price_change_24h_formatted": _format_percentage(price_change_24h),
                        "price_change_7d": price_change_7d,
                        "price_change_7d_formatted": _format_percentage(price_change_7d),
                    })
                
                top_list.append(item)
            
            return {
                "status": "success",
                "data": {
                    "type": "top_list",
                    "currency": currency,
                    "count": len(top_list),
                    "coins": top_list
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        else:
            # Fetch specific coin data
            if symbol_upper not in CRYPTO_MAP:
                # Try to search for the coin
                available = ", ".join(sorted(CRYPTO_MAP.keys()))
                raise ValueError(f"Unknown symbol '{symbol}'. Available: {available}")
            
            coin_id = CRYPTO_MAP[symbol_upper]
            coin_data = _fetch_coin_data(coin_id, vs_currency)
            
            market_data = coin_data.get("market_data", {})
            
            result = {
                "status": "success",
                "data": {
                    "type": "single_coin",
                    "symbol": symbol_upper,
                    "name": coin_data.get("name", ""),
                    "currency": currency,
                    "rank": market_data.get("market_cap_rank", 0),
                    "price": market_data.get("current_price", {}).get(vs_currency, 0),
                    "price_formatted": _format_currency(
                        market_data.get("current_price", {}).get(vs_currency, 0),
                        currency
                    ),
                    "market_cap": market_data.get("market_cap", {}).get(vs_currency, 0),
                    "market_cap_formatted": _format_currency(
                        market_data.get("market_cap", {}).get(vs_currency, 0),
                        currency
                    ),
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            if include_market_data:
                price_change_24h = market_data.get("price_change_percentage_24h", 0) or 0
                price_change_7d = market_data.get("price_change_percentage_7d", 0) or 0
                price_change_30d = market_data.get("price_change_percentage_30d", 0) or 0
                
                result["data"].update({
                    "volume_24h": market_data.get("total_volume", {}).get(vs_currency, 0),
                    "volume_formatted": _format_currency(
                        market_data.get("total_volume", {}).get(vs_currency, 0),
                        currency
                    ),
                    "circulating_supply": market_data.get("circulating_supply", 0),
                    "total_supply": market_data.get("total_supply"),
                    "max_supply": market_data.get("max_supply"),
                    "fully_diluted_valuation": market_data.get("fully_diluted_valuation", {}).get(vs_currency),
                    "fdv_formatted": _format_currency(
                        market_data.get("fully_diluted_valuation", {}).get(vs_currency, 0),
                        currency
                    ) if market_data.get("fully_diluted_valuation") else None,
                    "market_cap_dominance": market_data.get("market_cap_percentage", 0),
                    "price_change_24h": price_change_24h,
                    "price_change_24h_formatted": _format_percentage(price_change_24h),
                    "price_change_7d": price_change_7d,
                    "price_change_7d_formatted": _format_percentage(price_change_7d),
                    "price_change_30d": price_change_30d,
                    "price_change_30d_formatted": _format_percentage(price_change_30d),
                    "ath": market_data.get("ath", {}).get(vs_currency),
                    "ath_formatted": _format_currency(
                        market_data.get("ath", {}).get(vs_currency, 0),
                        currency
                    ) if market_data.get("ath") else None,
                    "ath_change_percentage": market_data.get("ath_change_percentage", {}).get(vs_currency),
                    "ath_date": market_data.get("ath_date", {}).get(vs_currency),
                })
            
            return result
    
    except ValueError as e:
        logger.warning(f"Market cap tracker validation error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "data": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    except requests.RequestException as e:
        logger.error(f"Market cap tracker API error: {e}")
        _log_lesson(f"market_cap_tracker API error: {e}")
        return {
            "status": "error",
            "error": f"API request failed: {str(e)}",
            "data": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    except Exception as e:
        logger.error(f"Market cap tracker unexpected error: {e}")
        _log_lesson(f"market_cap_tracker unexpected error: {e}")
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "data": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file."""
    try:
        import os
        os.makedirs("logs", exist_ok=True)  # ✅ Fixed: Ensure directory exists
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
