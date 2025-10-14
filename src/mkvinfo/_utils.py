from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from mkvinfo._errors import ExecutableNotFoundError, MKVInfoError

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import ParamSpec, TypeVar

    T = TypeVar("T")
    P = ParamSpec("P")

    def cache(_: Callable[P, T], /) -> Callable[P, T]: ...
else:
    from functools import cache


@cache
def mkvmerge_exe() -> Path:
    """Tiny wrapper that returns the path to `mkvmerge` executable."""
    exe = shutil.which("mkvmerge")
    if exe:  # pragma: no cover
        return Path(exe).resolve()
    msg = "`mkvmerge` executable not found in your system's $PATH."
    raise ExecutableNotFoundError(msg)


def mkvmerge_run(file: Path, *, exe: Path | None = None) -> bytes:  # pragma: no cover
    try:
        proc = subprocess.run(
            (
                exe if exe else mkvmerge_exe(),
                "--output-charset",
                "UTF-8",
                "-J",
                file,
            ),
            capture_output=True,
            check=True,
        )
        return proc.stdout
    except subprocess.CalledProcessError as e:
        msg = "An unexpected error occurred while running mkvmerge."
        raise MKVInfoError(msg) from e
