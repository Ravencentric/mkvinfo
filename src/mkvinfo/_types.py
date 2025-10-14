from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from mkvinfo._errors import ExecutableNotFoundError
from mkvinfo._utils import mkvmerge_run

if sys.version_info >= (3, 11):
    from enum import StrEnum as BaseStrEnum
else:
    from enum import Enum

    class BaseStrEnum(str, Enum):
        pass


if TYPE_CHECKING:
    from os import PathLike
    from typing import TypeAlias

    from typing_extensions import Self

    StrPath: TypeAlias = str | PathLike[str]


class StrEnum(BaseStrEnum):
    @classmethod
    def _missing_(cls, value: object) -> Self:
        # https://docs.python.org/3/library/enum.html#enum.Enum._missing_
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
            raise ValueError(msg)
        raise ValueError(msg)


@dataclass(frozen=True, kw_only=True, slots=True)
class Attachment:
    """Represents an attachment in a matroska file."""

    file_name: str
    id: int
    size: int
    content_type: str | None = None
    description: str | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class ContainerProperties:
    """Represents the properties of the container."""

    container_type: int | None = None
    date_local: datetime | None = None
    date_utc: datetime | None = None
    duration: int | None = None
    is_providing_timestamps: bool | None = None
    muxing_application: str | None = None
    timestamp_scale: int | None = None
    title: str | None = None
    writing_application: str | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class Container:
    """Represents the container."""

    recognized: bool = False
    supported: bool = False
    properties: ContainerProperties = field(default_factory=ContainerProperties)
    type: str | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class TrackProperties:
    """Represents the properties of a track."""

    alpha_mode: int | None = None
    audio_bits_per_sample: int | None = None
    audio_channels: int | None = None
    audio_emphasis: int | None = None
    audio_sampling_frequency: int | None = None
    cb_subsample: str | None = None
    chroma_siting: str | None = None
    chroma_subsample: str | None = None
    chromaticity_coordinates: str | None = None
    codec_delay: int | None = None
    codec_id: str | None = None
    codec_name: str | None = None
    content_encoding_algorithms: str | None = None
    color_bits_per_channel: int | None = None
    color_matrix_coefficients: int | None = None
    color_primaries: int | None = None
    color_range: int | None = None
    color_transfer_characteristics: int | None = None
    default_duration: int | None = None
    default_track: bool | None = None
    display_dimensions: str | None = None
    display_unit: int | None = None
    enabled_track: bool | None = None
    encoding: str | None = None
    forced_track: bool | None = None
    flag_hearing_impaired: bool | None = None
    flag_visual_impaired: bool | None = None
    flag_text_descriptions: bool | None = None
    flag_original: bool | None = None
    flag_commentary: bool | None = None
    language: str | None = None
    language_ietf: str | None = None
    max_content_light: int | None = None
    max_frame_light: int | None = None
    max_luminance: float | None = None
    min_luminance: float | None = None
    minimum_timestamp: int | None = None
    multiplexed_tracks: tuple[int, ...] | None = None
    number: int | None = None
    num_index_entries: int | None = None
    packetizer: str | None = None
    pixel_dimensions: str | None = None
    program_number: int | None = None
    projection_pose_pitch: float | None = None
    projection_pose_roll: float | None = None
    projection_pose_yaw: float | None = None
    projection_private: str | None = None
    projection_type: int | None = None
    stereo_mode: int | None = None
    stream_id: int | None = None
    sub_stream_id: int | None = None
    teletext_page: int | None = None
    text_subtitles: bool | None = None
    track_name: str | None = None
    uid: int | None = None
    white_color_coordinates: str | None = None


class TrackType(StrEnum):
    """Represents the type of a track."""

    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLES = "subtitles"

    def is_video(self) -> bool:
        """Check if this instance is a video track."""
        return self is TrackType.VIDEO

    def is_audio(self) -> bool:
        """Check if this instance is an audio track."""
        return self is TrackType.AUDIO

    def is_subtitles(self) -> bool:
        """Check if this instance is a subtitles track."""
        return self is TrackType.SUBTITLES


@dataclass(frozen=True, kw_only=True, slots=True)
class Track:
    """Represents a track in a matroska file."""

    codec: str
    id: int
    type: TrackType
    properties: TrackProperties = field(default_factory=TrackProperties)


@dataclass(frozen=True, kw_only=True, slots=True)
class MKVInfo:
    """
    Represents information about a matroska file as per the
    [`mkvmerge-identification-output-schema-v20.json`][0].

    The attributes represent exactly what's defined (or not defined)
    in the [`mkvmerge` documentation][1] and that schema.
    Please refer to those resources for details.

    [0]: https://mkvtoolnix.download/doc/mkvmerge-identification-output-schema-v20.json
    [1]: https://mkvtoolnix.download/doc/mkvmerge.html
    """

    file_name: str
    container: Container = field(default_factory=Container)
    attachments: tuple[Attachment, ...] = ()
    tracks: tuple[Track, ...] = ()
    identification_format_version: int | None = None

    @classmethod
    def from_json(cls, data: str | bytes, /) -> Self:
        """
        Create an instance of this class from JSON data.

        Parameters
        ----------
        data : str | bytes
            JSON data representing the instance of this class.

        Returns
        -------
        Self
            An instance of this class.

        """
        validator = TypeAdapter(cls)
        return validator.validate_json(data)

    @classmethod
    def from_file(
        cls,
        file: StrPath,
        /,
        *,
        mkvmerge: StrPath | None = None,
    ) -> Self:  # pragma: no cover
        """
        Create an instance of this class from a file.

        This method uses [`mkvmerge`][0] in a subprocess
        to extract the information.

        [0]: https://mkvtoolnix.download/doc/mkvmerge.html

        Parameters
        ----------
        file : StrPath
            Path to the file.
        mkvmerge : StrPath | None, optional
            Optional path to the `mkvmerge` executable. If provided,
            this path will be used instead of searching the system's `$PATH`.

        Returns
        -------
        Self
            An instance of this class.

        Raises
        ------
        FileNotFoundError
            If the provided file path does not exist or is not a valid file.
        ExecutableNotFoundError
            If the `mkvmerge` executable is not found.
        MKVInfoError
            For other errors that occur during the execution of the `mkvmerge`.

        """
        file = Path(file)
        if not file.is_file():
            raise FileNotFoundError(file)

        if mkvmerge is not None:
            mkvmerge = Path(mkvmerge)
            if not mkvmerge.is_file():
                msg = (
                    f"Provided mkvmerge path '{mkvmerge}' "
                    "does not exist or is not a valid file."
                )
                raise ExecutableNotFoundError(msg)

        data = mkvmerge_run(file, exe=mkvmerge)
        return cls.from_json(data)
