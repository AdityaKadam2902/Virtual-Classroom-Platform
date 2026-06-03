"""
app/services/storage.py
────────────────────────
Pluggable storage backend.
  • LocalStorage  – saves files to <instance>/uploads/  (development)
  • S3Storage     – uploads to AWS S3                   (production)

Switch with STORAGE_BACKEND env var.  Both expose the same interface so
route handlers never need to care which one is active.
"""
import os
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional
from urllib.parse import urljoin

from flask import current_app
from werkzeug.utils import secure_filename


def _safe_extension(filename: str) -> str:
    """Return lowercase extension without the dot, or ''."""
    return Path(filename).suffix.lstrip(".").lower()


def _unique_filename(original: str) -> str:
    """Generate a UUID-based filename that preserves the extension."""
    ext = _safe_extension(original)
    stem = str(uuid.uuid4()).replace("-", "")
    return f"{stem}.{ext}" if ext else stem


class StorageBackend(ABC):
    @abstractmethod
    def upload(self, file_obj: BinaryIO, original_filename: str, folder: str = "") -> dict:
        """
        Upload *file_obj* and return a dict:
            {
              "filename":    <stored filename>,
              "storage_key": <lookup key – path or S3 key>,
              "url":         <public or pre-signed URL>,
              "file_size":   <bytes>,
            }
        """

    @abstractmethod
    def delete(self, storage_key: str) -> None:
        """Remove a previously uploaded file."""

    @abstractmethod
    def get_url(self, storage_key: str, expiry_seconds: int = 3600) -> str:
        """Return a (possibly time-limited) URL for *storage_key*."""


# ── Local filesystem ──────────────────────────────────────────────────────────

class LocalStorage(StorageBackend):
    def _upload_dir(self, folder: str) -> Path:
        base = Path(current_app.instance_path) / current_app.config["LOCAL_UPLOAD_FOLDER"]
        target = (base / folder) if folder else base
        target.mkdir(parents=True, exist_ok=True)
        return target

    def upload(self, file_obj: BinaryIO, original_filename: str, folder: str = "") -> dict:
        safe_orig = secure_filename(original_filename)
        stored_name = _unique_filename(safe_orig)
        target_dir = self._upload_dir(folder)
        dest = target_dir / stored_name
        file_obj.seek(0)
        data = file_obj.read()
        dest.write_bytes(data)
        storage_key = str(Path(folder) / stored_name) if folder else stored_name
        return {
            "filename": stored_name,
            "storage_key": storage_key,
            "url": f"/uploads/{storage_key}",
            "file_size": len(data),
        }

    def delete(self, storage_key: str) -> None:
        base = Path(current_app.instance_path) / current_app.config["LOCAL_UPLOAD_FOLDER"]
        target = base / storage_key
        if target.exists():
            target.unlink()

    def get_url(self, storage_key: str, expiry_seconds: int = 3600) -> str:
        return f"/uploads/{storage_key}"


# ── AWS S3 ────────────────────────────────────────────────────────────────────

class S3Storage(StorageBackend):
    def __init__(self) -> None:
        import boto3
        self._s3 = boto3.client(
            "s3",
            region_name=current_app.config["AWS_S3_REGION"],
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
        )
        self._bucket = current_app.config["AWS_S3_BUCKET"]

    def upload(self, file_obj: BinaryIO, original_filename: str, folder: str = "") -> dict:
        safe_orig = secure_filename(original_filename)
        stored_name = _unique_filename(safe_orig)
        key = f"{folder}/{stored_name}" if folder else stored_name
        file_obj.seek(0)
        data = file_obj.read()
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)
        return {
            "filename": stored_name,
            "storage_key": key,
            "url": self.get_url(key),
            "file_size": len(data),
        }

    def delete(self, storage_key: str) -> None:
        self._s3.delete_object(Bucket=self._bucket, Key=storage_key)

    def get_url(self, storage_key: str, expiry_seconds: int = 3600) -> str:
        return self._s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": storage_key},
            ExpiresIn=expiry_seconds,
        )


# ── Factory ───────────────────────────────────────────────────────────────────

def get_storage() -> StorageBackend:
    """Return the active storage backend configured via STORAGE_BACKEND."""
    backend = current_app.config.get("STORAGE_BACKEND", "local")
    if backend == "s3":
        return S3Storage()
    return LocalStorage()
