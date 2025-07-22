from __future__ import annotations

from mkvinfo import TrackType


def test_track_type_methods() -> None:
    video = TrackType("video")
    assert video.is_video()
    assert not video.is_audio()
    assert not video.is_subtitles()

    audio = TrackType("aUDio")
    assert audio.is_audio()
    assert not audio.is_video()
    assert not audio.is_subtitles()

    subtitles = TrackType("SUBTITLES")
    assert subtitles.is_subtitles()
    assert not subtitles.is_video()
    assert not subtitles.is_audio()
