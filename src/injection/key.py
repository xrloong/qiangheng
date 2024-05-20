import typing

from writer import BaseWriter

Package = typing.NewType('package', type(typing))

Characters = typing.NewType('characters', tuple)

Quiet = typing.NewType('quiet', bool)
Writer = typing.NewType('writer', BaseWriter)

