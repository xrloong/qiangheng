from coding.Input import InputPlugin, FontVariance

from .FourCorner import FCCodeInfoEncoder
from .FourCorner import FCRadixParser

plugin = InputPlugin(
    method_name="fc",
    encoder_class=FCCodeInfoEncoder,
    radix_parser_class=FCRadixParser,
    font_variance=FontVariance.Traditional,
)

CodeInfoEncoder = plugin.CodeInfoEncoder
CodingRadixParser = plugin.CodingRadixParser
fontVariance = plugin.fontVariance
codeMappingInfoInterpreter = plugin.codeMappingInfoInterpreter
CodingSubstituteFileList = plugin.CodingSubstituteFileList
CodingRadixFileList = plugin.CodingRadixFileList
CodingAdjustFileList = plugin.CodingAdjustFileList
