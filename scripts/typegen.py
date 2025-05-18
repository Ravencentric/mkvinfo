from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen

from datamodel_code_generator import (
    DataModelType,
    InputFileType,
    PythonVersion,
    generate,
)
from datamodel_code_generator.format import Formatter

SCHEMA_URL = (
    "https://mkvtoolnix.download/doc/mkvmerge-identification-output-schema-v20.json"
)
SCHEMA_FILENAME = SCHEMA_URL.split("/")[-1]

with urlopen(SCHEMA_URL) as response:
    jsonschema = response.read().decode(encoding="utf-8")


output = Path(r"src\mkvinfo\_schema.py")
generate(
    jsonschema,
    input_filename=SCHEMA_FILENAME,
    input_file_type=InputFileType.JsonSchema,
    output=output,
    output_model_type=DataModelType.MsgspecStruct,
    target_python_version=PythonVersion.PY_310,
    use_field_description=True,
    use_union_operator=True,
    reuse_model=True,
    capitalise_enum_members=True,
    keyword_only=True,
    formatters=[Formatter.RUFF_CHECK, Formatter.RUFF_FORMAT],
    enable_version_header=True,
    enable_faux_immutability=True,
    use_title_as_name=True,
    treat_dot_as_module=True,
)
