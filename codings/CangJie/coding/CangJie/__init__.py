from coding.Input import InputPlugin, FontVariance

from .CangJie import CJCodeInfoEncoder, CJRadixParser

plugin = InputPlugin(
    method_name="cj",
    encoder_class=CJCodeInfoEncoder,
    radix_parser_class=CJRadixParser,
    font_variance=FontVariance.Traditional,
)
