from coding.Drawing import DrawingPlugin, FontVariance

from .StrokeOrder import SOCodeInfoEncoder
from .StrokeOrder import SORadixParser
from .StrokeOrder import SOCodeMappingInfoInterpreter

plugin = DrawingPlugin(
    method_name="dc",
    encoder_class=SOCodeInfoEncoder,
    radix_parser_class=SORadixParser,
    interpreter=SOCodeMappingInfoInterpreter(),
    font_variance=FontVariance.Traditional,
)
