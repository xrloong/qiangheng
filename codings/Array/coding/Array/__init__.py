from coding.Input import InputPlugin, FontVariance

from .Array import ARCodeInfoEncoder
from .Array import ARRadixParser

plugin = InputPlugin(
    method_name="ar",
    encoder_class=ARCodeInfoEncoder,
    radix_parser_class=ARRadixParser,
    font_variance=FontVariance.Traditional,
)

CodeInfoEncoder = plugin.CodeInfoEncoder
CodingRadixParser = plugin.CodingRadixParser
fontVariance = plugin.fontVariance
codeMappingInfoInterpreter = plugin.codeMappingInfoInterpreter
CodingSubstituteFileList = plugin.CodingSubstituteFileList
CodingRadixFileList = plugin.CodingRadixFileList
CodingAdjustFileList = plugin.CodingAdjustFileList
