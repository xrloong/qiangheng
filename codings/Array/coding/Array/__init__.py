from coding.Input import InputPlugin, FontVariance

from .Array import ARCodeInfoEncoder, ARRadixParser

plugin = InputPlugin(
    method_name="ar",
    encoder_class=ARCodeInfoEncoder,
    radix_parser_class=ARRadixParser,
    font_variance=FontVariance.Traditional,
)
