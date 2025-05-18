from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from syrupy.extensions.json import JSONSnapshotExtension

from mkvinfo import MKVInfo

if TYPE_CHECKING:
    from syrupy.session import SnapshotAssertion  # type: ignore[attr-defined]

SAMPLE_DIR = Path(__file__).parent / "samples"
SAMPLES = tuple(SAMPLE_DIR.glob("*.json"))


@pytest.mark.parametrize("sample", SAMPLES, ids=lambda p: p.name)
def test_mkvinfo(sample: Path, snapshot: SnapshotAssertion) -> None:
    obj = MKVInfo.from_json(sample.read_bytes())
    assert obj.to_dict() == snapshot(extension_class=JSONSnapshotExtension)
    assert MKVInfo.from_dict(obj.to_dict()) == obj
    assert MKVInfo.from_json(obj.to_json()) == obj
