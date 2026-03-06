import hmac
import hashlib
import json
import logging
import os

logger = logging.getLogger(__name__)

def generate_signature(payload: dict, secret: str) -> str:
    """
    Generates an HMAC SHA-256 signature for a JSON payload.
    The payload is serialized with sort_keys=True to ensure deterministic signatures.
    """
    serialized_payload = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hmac.new(secret.encode('utf-8'), serialized_payload, hashlib.sha256).hexdigest()

def validate_payload(payload: dict, signature: str) -> bool:
    """
    Validates the HMAC SHA-256 signature of a given payload.
    Invalid signatures are logged and return False.
    """
    secret = os.environ.get("THUNDER_PROTOCOL_SECRET")
    if not secret:
        logger.error("THUNDER_PROTOCOL_SECRET not set in environment.")
        return False
        
    expected_signature = generate_signature(payload, secret)
    
    if hmac.compare_digest(expected_signature, signature):
        return True
    else:
        logger.error("Invalid HMAC signature detected. Silently burning payload.")
        return False
