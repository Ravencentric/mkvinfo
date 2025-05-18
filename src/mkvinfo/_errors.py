from __future__ import annotations


class MKVInfoError(Exception):
    """Base exception for the mkvinfo library."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ExecutableNotFoundError(MKVInfoError):
    """Raised when the mkvmerge executable is not found."""
