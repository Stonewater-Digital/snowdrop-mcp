"""
Executive Summary: Google Sheets bridge that creates, reads, and writes fund-accounting ledger tabs via a GCP service account.

Inputs: action (str: init/read/write/get_balance), spreadsheet_url (str, optional),
        tab_name (str, optional), row_data (list, optional), spreadsheet_name (str, optional)
Outputs: dict with spreadsheet URL, row data, or balance sum depending on action
MCP Tool Name: ghost_ledger
"""
import os
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

from skills.utils import log_lesson, get_iso_timestamp, logger

# --- GCP OAuth Scopes ---
SCOPES: list[str] = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# --- Tab Headers ---
TAB_HEADERS: dict[str, list[str]] = {
    "THE VAULT": [
        "Timestamp",
        "Transaction ID",
        "Amount (USD)",
        "Counterparty",
        "Status",
        "Snowdrop Reasoning",
    ],
    "THE WATERING HOLE": [
        "Agent Name",
        "Wallet Address",
        "House Balance (TON)",
        "Labor Contribution",
        "Last Sip Date",
    ],
    "THE LOGIC LOG": [
        "Timestamp",
        "Entity",
        "Proposed Action",
        "Approval Status",
        "Decision",
    ],
    "GOODWILL": [
        "Recipient",
        "Gift Type",
        "Compute Cost",
        "Brand Value Score",
    ],
}

# --- MCP Tool Metadata ---
TOOL_META = {
    "name": "ghost_ledger",
    "description": (
        "Google Sheets fund-accounting bridge. Supports initializing a new ledger spreadsheet "
        "with structured tabs, reading tab data, appending rows, summing vault balances, and "
        "writing autonomous decision entries to THE LOGIC LOG tab for audit traceability."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["init", "read", "write", "batch_write", "get_balance", "log_decision"],
                "description": "Operation to perform on the ledger.",
            },
            "spreadsheet_url": {
                "type": "string",
                "description": "Full Google Sheets URL (required for read/write/get_balance).",
            },
            "tab_name": {
                "type": "string",
                "description": "Name of the worksheet tab (required for read/write).",
            },
            "row_data": {
                "type": "array",
                "items": {},
                "description": "List of cell values to append as a new row (required for write).",
            },
            "rows_data": {
                "type": "array",
                "items": {"type": "array", "items": {}},
                "description": "List of rows to append (required for batch_write).",
            },
            "spreadsheet_name": {
                "type": "string",
                "description": "Name for the new spreadsheet (required for init).",
            },
            "decision": {
                "type": "string",
                "description": "Human-readable description of the autonomous decision taken (required for log_decision).",
            },
            "reasoning": {
                "type": "string",
                "description": "Why this decision was made — the 'because' (required for log_decision).",
            },
            "outcome": {
                "type": "string",
                "description": "What happened as a result — ok, error, or a brief description (optional for log_decision).",
            },
        },
        "required": ["action"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}


def _get_client() -> gspread.Client:
    """Authorize and return a gspread client using a GCP service account.

    Checks GOOGLE_SERVICE_ACCOUNT_JSON first (JSON string — works in Railway/cloud
    where file mounts aren't available), then falls back to GCP_SERVICE_ACCOUNT_FILE
    (local file path — used on HP).

    Returns:
        gspread.Client: An authorized Google Sheets API client.

    Raises:
        ValueError: If neither credential env var is set.
    """
    import json

    sa_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        info = json.loads(sa_json)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        return gspread.authorize(creds)

    sa_file = os.getenv("GCP_SERVICE_ACCOUNT_FILE")
    if sa_file:
        creds = Credentials.from_service_account_file(sa_file, scopes=SCOPES)
        return gspread.authorize(creds)

    raise ValueError(
        "Set GOOGLE_SERVICE_ACCOUNT_JSON (JSON string) or GCP_SERVICE_ACCOUNT_FILE (file path)"
    )


def init_ledger(spreadsheet_name: str) -> dict:
    """Create a new Google Sheets ledger with the four canonical fund-accounting tabs.

    Creates the spreadsheet, renames the default sheet to "THE VAULT", adds the
    remaining three tabs, and writes column headers to each.

    Args:
        spreadsheet_name: Display name for the new Google Spreadsheet.

    Returns:
        dict: Result dict containing the new spreadsheet URL on success.
    """
    try:
        client = _get_client()
        spreadsheet = client.create(spreadsheet_name)

        # Rename the default first sheet, then add the rest
        tab_names = list(TAB_HEADERS.keys())
        first_sheet = spreadsheet.sheet1
        first_sheet.update_title(tab_names[0])
        first_sheet.append_row(TAB_HEADERS[tab_names[0]])

        for tab_name in tab_names[1:]:
            sheet = spreadsheet.add_worksheet(title=tab_name, rows=1000, cols=20)
            sheet.append_row(TAB_HEADERS[tab_name])

        # Share publicly readable so Thunder can open the link directly
        spreadsheet.share(None, perm_type="anyone", role="reader")

        url: str = spreadsheet.url
        logger.info(f"ghost_ledger.init_ledger: created '{spreadsheet_name}' at {url}")
        return {
            "status": "success",
            "data": {"spreadsheet_url": url, "tabs_created": tab_names},
            "timestamp": get_iso_timestamp(),
        }

    except Exception as e:
        logger.error(f"ghost_ledger.init_ledger failed: {e}")
        log_lesson(f"ghost_ledger.init_ledger: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }


def read_tab(spreadsheet_url: str, tab_name: str) -> dict:
    """Read all rows from a named worksheet tab and return them as a list of dicts.

    The first row is treated as the header row and used as dict keys.

    Args:
        spreadsheet_url: Full URL of the Google Spreadsheet.
        tab_name: Exact name of the worksheet tab to read.

    Returns:
        dict: Result dict with a "rows" list of dicts (header keys, cell values).
    """
    try:
        client = _get_client()
        spreadsheet = client.open_by_url(spreadsheet_url)
        sheet = spreadsheet.worksheet(tab_name)
        rows: list[dict] = sheet.get_all_records()

        logger.info(f"ghost_ledger.read_tab: read {len(rows)} rows from '{tab_name}'")
        return {
            "status": "success",
            "data": {"tab_name": tab_name, "rows": rows, "row_count": len(rows)},
            "timestamp": get_iso_timestamp(),
        }

    except Exception as e:
        logger.error(f"ghost_ledger.read_tab failed: {e}")
        log_lesson(f"ghost_ledger.read_tab: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }


def write_entry(spreadsheet_url: str, tab_name: str, row_data: list) -> dict:
    """Append a single row of data to a named worksheet tab.

    Args:
        spreadsheet_url: Full URL of the Google Spreadsheet.
        tab_name: Exact name of the worksheet tab to write to.
        row_data: Ordered list of cell values matching the tab's column schema.

    Returns:
        dict: Result dict confirming the row was appended.
    """
    try:
        client = _get_client()
        spreadsheet = client.open_by_url(spreadsheet_url)
        sheet = spreadsheet.worksheet(tab_name)
        sheet.append_row(row_data)

        logger.info(f"ghost_ledger.write_entry: appended row to '{tab_name}'")
        return {
            "status": "success",
            "data": {"tab_name": tab_name, "row_appended": row_data},
            "timestamp": get_iso_timestamp(),
        }

    except Exception as e:
        logger.error(f"ghost_ledger.write_entry failed: {e}")
        log_lesson(f"ghost_ledger.write_entry: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }



def batch_write_entries(spreadsheet_url: str, tab_name: str, rows_data: list) -> dict:
    """Append multiple rows of data to a named worksheet tab."""
    try:
        client = _get_client()
        spreadsheet = client.open_by_url(spreadsheet_url)
        sheet = spreadsheet.worksheet(tab_name)
        sheet.append_rows(rows_data)

        logger.info(f"ghost_ledger.batch_write: appended {len(rows_data)} rows to {tab_name}")
        return {
            "status": "success",
            "data": {"tab_name": tab_name, "rows_appended": len(rows_data)},
            "timestamp": get_iso_timestamp(),
        }

    except Exception as e:
        logger.error(f"ghost_ledger.batch_write failed: {e}")
        log_lesson(f"ghost_ledger.batch_write: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }

def get_balance(spreadsheet_url: str) -> dict:
    """Sum the "Amount (USD)" column in THE VAULT tab to compute the ledger balance.

    Reads all rows from THE VAULT, filters for valid numeric entries in the
    "Amount (USD)" column, and returns the sum as the current ledger balance.

    Args:
        spreadsheet_url: Full URL of the Google Spreadsheet.

    Returns:
        dict: Result dict with "ledger_balance" (float, sum of Amount (USD) column).
    """
    try:
        client = _get_client()
        spreadsheet = client.open_by_url(spreadsheet_url)
        sheet = spreadsheet.worksheet("THE VAULT")
        rows: list[dict] = sheet.get_all_records()

        ledger_balance: float = 0.0
        for row in rows:
            raw = row.get("Amount (USD)", 0)
            try:
                ledger_balance += float(raw)
            except (TypeError, ValueError):
                pass  # Skip non-numeric cells

        logger.info(f"ghost_ledger.get_balance: ledger_balance={ledger_balance:.2f}")
        return {
            "status": "success",
            "data": {
                "ledger_balance": round(ledger_balance, 2),
                "rows_processed": len(rows),
            },
            "timestamp": get_iso_timestamp(),
        }

    except Exception as e:
        logger.error(f"ghost_ledger.get_balance failed: {e}")
        log_lesson(f"ghost_ledger.get_balance: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }


def ghost_ledger(action: str, **kwargs: Any) -> dict:
    """Dispatch a ledger operation based on the action parameter.

    Acts as the single MCP entry point for all Ghost Ledger operations, routing
    to the appropriate internal function based on the action value.

    Args:
        action: One of "init", "read", "write", or "get_balance".
        **kwargs: Additional arguments forwarded to the underlying function:
            - spreadsheet_name (str): Required for "init".
            - spreadsheet_url (str): Required for "read", "write", "get_balance".
            - tab_name (str): Required for "read" and "write".
            - row_data (list): Required for "write".

    Returns:
        dict: Result dict from the dispatched sub-function, or an error dict if
        the action is unrecognized or required kwargs are missing.
    """
    try:
        if action == "init":
            spreadsheet_name = kwargs.get("spreadsheet_name")
            if not spreadsheet_name:
                raise ValueError("spreadsheet_name is required for action='init'")
            return init_ledger(spreadsheet_name=spreadsheet_name)

        elif action == "read":
            spreadsheet_url = kwargs.get("spreadsheet_url")
            tab_name = kwargs.get("tab_name")
            if not spreadsheet_url or not tab_name:
                raise ValueError("spreadsheet_url and tab_name are required for action='read'")
            return read_tab(spreadsheet_url=spreadsheet_url, tab_name=tab_name)

        elif action == "write":
            spreadsheet_url = kwargs.get("spreadsheet_url")
            tab_name = kwargs.get("tab_name")
            row_data = kwargs.get("row_data")
            if not spreadsheet_url or not tab_name or row_data is None:
                raise ValueError("spreadsheet_url, tab_name, and row_data are required for action='write'")
            return write_entry(
                spreadsheet_url=spreadsheet_url,
                tab_name=tab_name,
                row_data=row_data,
            )

        elif action == "get_balance":
            spreadsheet_url = kwargs.get("spreadsheet_url")
            if not spreadsheet_url:
                raise ValueError("spreadsheet_url is required for action='get_balance'")
            return get_balance(spreadsheet_url=spreadsheet_url)

        elif action == "log_decision":
            decision = kwargs.get("decision", "")
            reasoning = kwargs.get("reasoning", "")
            outcome = kwargs.get("outcome", "")
            spreadsheet_url = kwargs.get("spreadsheet_url") or os.environ.get("GHOST_LEDGER_URL", "")
            if not decision or not reasoning:
                raise ValueError("decision and reasoning are required for action='log_decision'")
            if not spreadsheet_url:
                raise ValueError("spreadsheet_url is required for log_decision (or set GHOST_LEDGER_URL)")
            client = _get_client()
            sheet = client.open_by_url(spreadsheet_url)
            try:
                ws = sheet.worksheet("THE LOGIC LOG")
            except Exception:
                ws = sheet.add_worksheet(title="THE LOGIC LOG", rows=1000, cols=5)
                ws.append_row(["Timestamp", "Decision", "Reasoning", "Outcome", "Agent"])
            ts = get_iso_timestamp()
            ws.append_row([ts, decision, reasoning, outcome, "Snowdrop"])
            logger.info("LOGIC LOG: %s — %s", decision, reasoning)
            return {
                "status": "ok",
                "data": {"logged": True, "ts": ts, "decision": decision},
                "timestamp": ts,
            }

        else:
            raise ValueError(f"Unknown action '{action}'. Must be one of: init, read, write, batch_write, get_balance, log_decision")

    except Exception as e:
        logger.error(f"ghost_ledger failed: {e}")
        log_lesson(f"ghost_ledger: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }


