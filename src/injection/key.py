import typing

from writer import BaseWriter

Package = typing.NewType('package', type(typing))

Quiet = typing.NewType('quiet', bool)
Writer = typing.NewType('writer', BaseWriter)

