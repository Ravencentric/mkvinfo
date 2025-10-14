from __future__ import annotations


class MKVInfoError(Exception):
    """Base exception for the mkvinfo library."""

    __module__ = "mkvinfo"

    def __init_subclass__(cls) -> None:
        # Ensure subclasses also appear as part of the public 'mkvinfo' module
        # in tracebacks, instead of the internal implementation module.
        cls.__module__ = "mkvinfo"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ExecutableNotFoundError(MKVInfoError):
    """Raised when the mkvmerge executable is not found."""
