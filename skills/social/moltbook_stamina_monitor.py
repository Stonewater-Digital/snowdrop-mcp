"""
# Moltbook Stamina Monitor
# Executive Summary: A lightweight sub-agent that monitors Snowdrop's API rate limits.
# It reads the RATE LIMITS (STAMINA) tab in Google Sheets, analyzes the quota burn rate
# using a cheap/fast model (gemini-2.5-flash), and alerts the user if Snowdrop is at risk of a ban.

## Table of Contents
1. `moltbook_stamina_monitor` (MCP tool entrypoint)
2. `_fetch_rate_limits`
3. `_analyze_stamina`
4. `_trigger_alert`
"""
import os
import json
import logging
import requests
from datetime import datetime, timezone

from config.models import resolve_model
from skills.social.moltbook_engagement_sheet import _get_client, SHEET_ID, TAB_RATE_LIMITS

logger = logging.getLogger("snowdrop.social.ratelimit")
logger.setLevel(logging.INFO)

TOOL_META = {
    "name": "moltbook_stamina_monitor",
    "description": "Monitors Moltbook API rate limits (stamina) from the Google Sheet and generates a 1-sentence health summary using a cheap model.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "summary": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "summary", "timestamp"],
    },
}

def _fetch_rate_limits(limit: int = 50) -> list:
    """Reads the last N rows from the RATE LIMITS tab."""
    try:
        gc = _get_client()
        sheet = gc.open_by_key(SHEET_ID)
        ws = sheet.worksheet(TAB_RATE_LIMITS)
        rows = ws.get_all_records()
        return rows[-limit:] if rows else []
    except Exception as e:
        logger.error(f"Failed to fetch rate limits: {e}")
        return []

def _analyze_stamina(recent_logs: list) -> str:
    """Uses a cheap OpenRouter model to evaluate burn rate."""
    if not recent_logs:
        return "No stamina data logged yet. Snowdrop's quota is likely intact."
        
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("OPENROUTER_API_KEY not found. Performing basic rule-based analysis.")
        last = recent_logs[-1]
        try:
            rem = int(last.get("Remaining", 100))
            if rem < 20:
                return f"WARNING: Quota is low. Only {rem} remaining on {last.get('Endpoint')}."
            return "Stamina appears healthy based on basic checks."
        except:
            return "Stamina appears healthy based on basic checks."
            
    prompt = f"""
Analyze the following JSON log of recent API rate limit data from an AI agent's social network interactions.
Data format is [Date, Endpoint, Limit, Remaining, Reset Time].

Data: {json.dumps(recent_logs)}

Task:
Are we burning quota too fast or at risk of a ban? Output ONLY a 1-sentence health summary.
"""
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": resolve_model("scout"),
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Error analyzing stamina: HTTP {resp.status_code} - {resp.text}"
    except Exception as e:
        return f"Error connecting to OpenRouter: {str(e)}"

def _trigger_alert(summary: str):
    """Sends a Slack/Telegram alert if the summary sounds dangerous."""
    # We would use the thunder_signal skill or raw API here.
    # For now, just logging critically.
    if "risk" in summary.lower() or "warning" in summary.lower() or "low" in summary.lower():
        logger.critical(f"STAMINA ALERT: {summary}")

def moltbook_stamina_monitor() -> dict:
    """Entry point for the stamina monitor."""
    ts = datetime.now(timezone.utc).isoformat()
    logger.info("Running Moltbook stamina monitor...")
    
    logs = _fetch_rate_limits()
    summary = _analyze_stamina(logs)
    
    _trigger_alert(summary)
    
    return {
        "status": "ok",
        "summary": summary,
        "timestamp": ts
    }
    
if __name__ == "__main__":
    # If run standalone as a cron job
    res = moltbook_stamina_monitor()
    print(json.dumps(res, indent=2))
