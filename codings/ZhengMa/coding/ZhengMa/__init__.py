from coding.Input import InputPlugin, FontVariance

from .ZhengMa import ZMCodeInfoEncoder
from .ZhengMa import ZMRadixParser

plugin = InputPlugin(
    method_name="zm",
    encoder_class=ZMCodeInfoEncoder,
    radix_parser_class=ZMRadixParser,
    font_variance=FontVariance.Simplified,
    has_fast_file=True,
)

CodeInfoEncoder = plugin.CodeInfoEncoder
CodingRadixParser = plugin.CodingRadixParser
fontVariance = plugin.fontVariance
codeMappingInfoInterpreter = plugin.codeMappingInfoInterpreter
CodingSubstituteFileList = plugin.CodingSubstituteFileList
CodingRadixFileList = plugin.CodingRadixFileList
CodingAdjustFileList = plugin.CodingAdjustFileList
CodingFastFile = plugin.CodingFastFile
