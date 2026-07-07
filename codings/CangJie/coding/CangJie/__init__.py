from coding.Input import InputPlugin, FontVariance

from .CangJie import CJCodeInfoEncoder
from .CangJie import CJRadixParser

plugin = InputPlugin(
    method_name="cj",
    encoder_class=CJCodeInfoEncoder,
    radix_parser_class=CJRadixParser,
    font_variance=FontVariance.Traditional,
)

CodeInfoEncoder = plugin.CodeInfoEncoder
CodingRadixParser = plugin.CodingRadixParser
fontVariance = plugin.fontVariance
codeMappingInfoInterpreter = plugin.codeMappingInfoInterpreter
CodingSubstituteFileList = plugin.CodingSubstituteFileList
CodingRadixFileList = plugin.CodingRadixFileList
CodingAdjustFileList = plugin.CodingAdjustFileList
