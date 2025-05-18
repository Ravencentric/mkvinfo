# mkvinfo

[![PyPI - Version](https://img.shields.io/pypi/v/mkvinfo?link=https%3A%2F%2Fpypi.org%2Fproject%2Fmkvinfo%2F)](https://pypi.org/project/mkvinfo/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkvinfo)
![License](https://img.shields.io/github/license/Ravencentric/mkvinfo)
![PyPI - Types](https://img.shields.io/pypi/types/mkvinfo)

![GitHub Build Workflow Status](https://img.shields.io/github/actions/workflow/status/Ravencentric/mkvinfo/release.yml)
![GitHub Tests Workflow Status](https://img.shields.io/github/actions/workflow/status/ravencentric/mkvinfo/tests.yml?label=tests)
[![codecov](https://codecov.io/gh/Ravencentric/mkvinfo/graph/badge.svg?token=96UDXZHP41)](https://codecov.io/gh/Ravencentric/mkvinfo)

Python library for probing [matroska](https://www.matroska.org/index.html) files with [`mkvmerge`](https://mkvtoolnix.download/doc/mkvmerge.html).

## Installation

`mkvinfo` is available on [PyPI](https://pypi.org/project/mkvinfo/), so you can simply use [pip](https://github.com/pypa/pip) to install it.

```sh
pip install mkvinfo
```

## Usage

```py
from mkvinfo import MKVInfo

mkv = MKVInfo.from_file("./Big Buck Bunny, Sunflower version.mkv")

assert mkv.file_name == "Big Buck Bunny, Sunflower version.mkv"
assert mkv.container.properties.title == "Big Buck Bunny, Sunflower version"
assert mkv.container.properties.writing_application == "mkvmerge v92.0 ('Everglow') 64-bit"

for track in mkv.tracks:
    print(f"{track.id} - {track.codec}")
    #> 0 - AVC/H.264/MPEG-4p10
    #> 1 - MP3
    #> 2 - AC-3
```

Checkout the complete documentation [here](https://ravencentric.cc/mkvinfo/).

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See [LICENSE](https://github.com/Ravencentric/mkvinfo/blob/main/LICENSE) for more information.