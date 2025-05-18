"""Python library for probing matroska files with `mkvmerge`."""

from __future__ import annotations

from mkvinfo._errors import ExecutableNotFoundError, MKVInfoError
from mkvinfo._types import (
    Attachment,
    Container,
    ContainerProperties,
    MKVInfo,
    Track,
    TrackProperties,
    TrackType,
)

__all__ = (
    "Attachment",
    "Container",
    "ContainerProperties",
    "ExecutableNotFoundError",
    "MKVInfo",
    "MKVInfoError",
    "Track",
    "TrackProperties",
    "TrackType",
)
