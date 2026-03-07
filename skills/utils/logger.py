import json
import logging
import sys
import uuid
import contextvars
from datetime import datetime, timezone
from typing import Any, Dict

# Context variable to store current trace_id
_trace_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar('trace_id', default="")

def set_trace_id(trace_id: str) -> None:
    """Set the trace ID for the current context."""
    _trace_id_ctx.set(trace_id)

def get_trace_id() -> str:
    """Get the current trace ID, generating a new one if not set."""
    tid = _trace_id_ctx.get()
    if not tid:
        tid = str(uuid.uuid4())
        _trace_id_ctx.set(tid)
    return tid

def clear_trace_id() -> None:
    """Clear the current trace ID."""
    _trace_id_ctx.set("")

class JSONFormatter(logging.Formatter):
    """Structured JSON formatter with trace ID support."""
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": get_trace_id(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        # Add extra arguments passed via extra dict safely
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_data.update(record.extra_data)

        return json.dumps(log_data)

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Get a JSON-formatted logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger
