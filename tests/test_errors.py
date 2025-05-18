from __future__ import annotations

import pytest

from mkvinfo import ExecutableNotFoundError, MKVInfo
from mkvinfo._utils import mkvmerge_exe


def test_file_not_found_error() -> None:
    with pytest.raises(FileNotFoundError):
        MKVInfo.from_file("./foo/bar")


def test_exe_not_found_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PATH")
    with pytest.raises(ExecutableNotFoundError):
        mkvmerge_exe()
