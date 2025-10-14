!!! note

    You'll notice right away that there are absolutely **no** docstrings within these classes. The main reason for that was me being lazy. An additional, compounding factor is that many of these attributes actually lack any description even in the source material – [the `mkvmerge` identification output schema v20](https://mkvtoolnix.download/doc/mkvmerge-identification-output-schema-v20.json), which this library's structure is based on.

    Because of the direct mapping to that schema (and, well, the laziness), I haven't attempted to document them here. The attributes represent exactly what's defined (or *not* defined) in the `mkvmerge` documentation and that schema. Please refer to those resources for details.

::: mkvinfo.MKVInfo
::: mkvinfo.Attachment
::: mkvinfo.Container
::: mkvinfo.ContainerProperties
::: mkvinfo.Track
::: mkvinfo.TrackProperties
::: mkvinfo.TrackType
