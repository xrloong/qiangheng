from coding.Drawing import DrawingPlugin, FontVariance

from .DynamicComposition import DCCodeInfoEncoder
from .DynamicComposition import DCRadixParser
from .DynamicComposition import DCCodeMappingInfoInterpreter

plugin = DrawingPlugin(
    method_name="dc",
    encoder_class=DCCodeInfoEncoder,
    radix_parser_class=DCRadixParser,
    interpreter=DCCodeMappingInfoInterpreter(),
    font_variance=FontVariance.Traditional,
)
