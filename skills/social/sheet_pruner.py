"""
# Sheet Pruner
# Executive Summary: Prevents data bloat in Snowdrop's Command Center by removing old log entries.
# Specifically targets the 'RATE LIMITS (STAMINA)' tab to delete rows older than a specified retention period.

## Table of Contents
1. `prune_rate_limits`
2. `sheet_pruner` (MCP tool entrypoint)
"""

import os
import logging
from datetime import datetime, timezone, timedelta
from skills.social.moltbook_engagement_sheet import _get_client, SHEET_ID, TAB_RATE_LIMITS

logger = logging.getLogger("snowdrop.social.pruner")
logger.setLevel(logging.INFO)

TOOL_META = {
    "name": "sheet_pruner",
    "description": "Prevents data bloat by autonomously removing logs older than the retention period from the Command Center.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "retention_days": {"type": "integer", "description": "Number of days to keep data. Defaults to 7."}
        },
        "required": [],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "rows_deleted": {"type": "integer"},
            "tab_name": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "rows_deleted", "tab_name", "timestamp"],
    },
}

def prune_rate_limits(retention_days: int = 7) -> int:
    """
    Reads the RATE LIMITS tab, filters out rows older than retention_days,
    and updates the sheet with the retained rows to avoid cell limit exhaustion.
    """
    try:
        gc = _get_client()
        sheet = gc.open_by_key(SHEET_ID)
        ws = sheet.worksheet(TAB_RATE_LIMITS)
    except Exception as e:
        logger.error(f"Failed to access sheet for pruning: {e}")
        return 0

    all_values = ws.get_all_values()
    if len(all_values) <= 1:
        # Only header or empty
        return 0

    headers = all_values[0]
    data_rows = all_values[1:]
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)
    
    retained_rows = []
    rows_deleted = 0
    
    for row in data_rows:
        if not row or not row[0]:
            continue
        try:
            # Expected format: "%Y-%m-%d %H:%M:%S"
            row_date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            if row_date >= cutoff_date:
                retained_rows.append(row)
            else:
                rows_deleted += 1
        except ValueError:
            # If date format is weird, keep the row to be safe
            retained_rows.append(row)

    if rows_deleted > 0:
        # Clear the sheet and rewrite
        ws.clear()
        ws.update(range_name="A1", values=[headers] + retained_rows)
        logger.info(f"Pruned {rows_deleted} rows from {TAB_RATE_LIMITS}. Retained {len(retained_rows)} rows.")
    else:
        logger.info(f"No rows older than {retention_days} days found in {TAB_RATE_LIMITS}.")

    return rows_deleted

def sheet_pruner(retention_days: int = 7) -> dict:
    """Entry point for the sheet pruner."""
    ts = datetime.now(timezone.utc).isoformat()
    
    deleted = prune_rate_limits(retention_days)
    
    return {
        "status": "ok",
        "rows_deleted": deleted,
        "tab_name": TAB_RATE_LIMITS,
        "timestamp": ts,
        "trace_id": "pruner-" + str(int(datetime.now(timezone.utc).timestamp()))
    }

if __name__ == "__main__":
    import json
    res = sheet_pruner()
    print(json.dumps(res, indent=2))
