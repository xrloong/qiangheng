from coding.Input import InputPlugin, FontVariance

from .Boshiamy import BSCodeInfoEncoder
from .Boshiamy import BSRadixParser

plugin = InputPlugin(
    method_name="bs",
    encoder_class=BSCodeInfoEncoder,
    radix_parser_class=BSRadixParser,
    font_variance=FontVariance.Traditional,
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
