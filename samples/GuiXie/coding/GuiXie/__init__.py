from coding.Input import InputPlugin, FontVariance

from .GuiXie import GXCodeInfoEncoder
from .GuiXie import GXRadixParser

plugin = InputPlugin(
    method_name="gx",
    encoder_class=GXCodeInfoEncoder,
    radix_parser_class=GXRadixParser,
    font_variance=FontVariance.Traditional,
    method_dir="samples/GuiXie/qhdata/",
)
