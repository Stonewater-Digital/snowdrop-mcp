"""Firebase Cloud Storage upload skill.

Uploads a base64-encoded file to Firebase Cloud Storage and returns
a signed download URL valid for 7 days.
"""

import base64
import json
import logging
import os
from datetime import datetime, timedelta, timezone

import firebase_admin
from firebase_admin import credentials as fb_credentials
from firebase_admin import storage

logger = logging.getLogger("snowdrop.firebase_storage_upload")

TOOL_META = {
    "name": "firebase_storage_upload",
    "description": "Upload a base64-encoded file to Firebase Cloud Storage. Returns the storage path and a signed download URL valid for 7 days.",
    "tier": "free",
}

_fb_app = None


def _get_fb_app():
    """Return initialized firebase_admin app. Idempotent."""
    global _fb_app
    if _fb_app is not None:
        return _fb_app
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        cred = fb_credentials.Certificate(json.loads(sa_json))
        _fb_app = firebase_admin.initialize_app(cred)
    else:
        _fb_app = firebase_admin.initialize_app()
    return _fb_app


def _get_credentials():
    """Return google.oauth2 credentials. ADC-first (Cloud Run), JSON fallback (local)."""
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_info(json.loads(sa_json))
    return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def firebase_storage_upload(
    destination_path: str,
    content_base64: str,
    content_type: str = "application/octet-stream",
    bucket_name: str | None = None,
) -> dict:
    """Upload a base64-encoded file to Firebase Cloud Storage.

    Decodes the base64 content, uploads it to the specified path in Cloud Storage,
    and generates a signed URL valid for 7 days. The signed URL allows unauthenticated
    HTTP GET access to the file without requiring Firebase credentials.

    Signed URL generation requires that the service account credentials contain a
    private key (i.e., GOOGLE_SERVICE_ACCOUNT_JSON is set with a full service account
    key file). On Cloud Run using ADC with a compute service account, you must use
    google.auth.iam.Signer with the service account email instead; in that case this
    skill falls back to a public GCS URL if signing is unavailable.

    Args:
        destination_path: Path within the bucket to store the file, e.g.
            "uploads/images/photo.jpg" or "reports/2024/q4.pdf".
            Do not include a leading "/".
        content_base64: Base64-encoded file content. Standard or URL-safe encoding
            is accepted. Padding characters are optional.
        content_type: MIME type of the uploaded file, e.g. "image/jpeg",
            "application/pdf", "text/csv". Defaults to "application/octet-stream".
        bucket_name: Firebase Storage bucket name without the "gs://" prefix, e.g.
            "my-project.appspot.com". If not provided, reads from the
            FIREBASE_STORAGE_BUCKET environment variable.

    Returns:
        dict: Standard Snowdrop response envelope.
            On success: {
                "status": "ok",
                "data": {
                    "bucket": str,
                    "path": str,
                    "content_type": str,
                    "size_bytes": int,
                    "signed_url": str,
                    "expires_at": str (ISO8601)
                },
                "timestamp": str
            }
            On error: {"status": "error", "data": {"error": str}, "timestamp": str}

    Raises:
        ValueError: If bucket_name cannot be resolved or content_base64 is invalid.
        google.cloud.exceptions.GoogleCloudError: If the Cloud Storage API returns
            an error.

    Example:
        >>> import base64
        >>> content = base64.b64encode(b"Hello, World!").decode()
        >>> result = firebase_storage_upload(
        ...     destination_path="test/hello.txt",
        ...     content_base64=content,
        ...     content_type="text/plain",
        ... )
        >>> result["status"]
        'ok'
        >>> result["data"]["path"]
        'test/hello.txt'
        >>> result["data"]["signed_url"].startswith("https://")
        True
    """
    logger.info(
        "firebase_storage_upload entered | destination_path=%s content_type=%s",
        destination_path, content_type,
    )

    resolved_bucket = bucket_name or os.environ.get("FIREBASE_STORAGE_BUCKET")
    if not resolved_bucket:
        msg = "bucket_name not provided and FIREBASE_STORAGE_BUCKET is not set."
        logger.error("firebase_storage_upload error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    # Decode base64 content — support both standard and URL-safe variants with missing padding
    try:
        # Add padding if needed
        padded = content_base64 + "=" * ((-len(content_base64)) % 4)
        file_bytes = base64.b64decode(padded.replace("-", "+").replace("_", "/"))
    except Exception as decode_exc:
        msg = f"Failed to decode base64 content: {decode_exc}"
        logger.error("firebase_storage_upload error: %s", msg)
        return {"status": "error", "data": {"error": msg}, "timestamp": _now()}

    try:
        _get_fb_app()

        bucket = storage.bucket(name=resolved_bucket)
        blob = bucket.blob(destination_path)

        blob.upload_from_string(file_bytes, content_type=content_type)
        logger.info(
            "firebase_storage_upload blob uploaded | bucket=%s path=%s size=%d",
            resolved_bucket, destination_path, len(file_bytes),
        )

        expiration = timedelta(days=7)
        expires_at = datetime.now(timezone.utc) + expiration

        # generate_signed_url requires a service account with a private key.
        # On Cloud Run with ADC, we attempt signing via google.auth.iam credentials.
        try:
            signed_url = blob.generate_signed_url(
                expiration=expiration,
                method="GET",
                version="v4",
            )
        except Exception as sign_exc:
            # Fallback: attempt IAM-based signing for Cloud Run ADC environments
            logger.warning(
                "firebase_storage_upload standard signing failed (%s); attempting IAM signing",
                sign_exc,
            )
            try:
                import google.auth
                import google.auth.transport.requests
                from google.auth.iam import Signer
                from google.auth.credentials import TokenState

                auth_creds, project = google.auth.default()
                auth_creds.refresh(google.auth.transport.requests.Request())

                service_account_email = getattr(auth_creds, "service_account_email", None)
                if not service_account_email:
                    raise ValueError("Cannot determine service account email for IAM signing.")

                signer = Signer(
                    request=google.auth.transport.requests.Request(),
                    credentials=auth_creds,
                    service_account_email=service_account_email,
                )

                from google.oauth2 import service_account as sa_module
                iam_creds = sa_module.Credentials(
                    signer=signer,
                    service_account_email=service_account_email,
                    token_uri="https://oauth2.googleapis.com/token",
                )
                signed_url = blob.generate_signed_url(
                    expiration=expiration,
                    method="GET",
                    version="v4",
                    credentials=iam_creds,
                )
            except Exception as iam_exc:
                # Last resort: return a public GCS URI (requires bucket/blob to be public)
                logger.warning(
                    "firebase_storage_upload IAM signing also failed (%s); returning public GCS URI",
                    iam_exc,
                )
                signed_url = f"https://storage.googleapis.com/{resolved_bucket}/{destination_path}"
                expires_at = datetime.now(timezone.utc)  # not a real expiry

        logger.info("firebase_storage_upload success | path=%s", destination_path)
        return {
            "status": "ok",
            "data": {
                "bucket": resolved_bucket,
                "path": destination_path,
                "content_type": content_type,
                "size_bytes": len(file_bytes),
                "signed_url": signed_url,
                "expires_at": expires_at.isoformat(),
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error("firebase_storage_upload error: %s", exc, exc_info=True)
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _now()}
