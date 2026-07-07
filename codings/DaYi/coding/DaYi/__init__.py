from coding.Input import InputPlugin, FontVariance

from .DaYi import DYCodeInfoEncoder
from .DaYi import DYRadixParser

plugin = InputPlugin(
    method_name="dy",
    encoder_class=DYCodeInfoEncoder,
    radix_parser_class=DYRadixParser,
    font_variance=FontVariance.Traditional,
)

CodeInfoEncoder = plugin.CodeInfoEncoder
CodingRadixParser = plugin.CodingRadixParser
fontVariance = plugin.fontVariance
codeMappingInfoInterpreter = plugin.codeMappingInfoInterpreter
CodingSubstituteFileList = plugin.CodingSubstituteFileList
CodingRadixFileList = plugin.CodingRadixFileList
CodingAdjustFileList = plugin.CodingAdjustFileList
