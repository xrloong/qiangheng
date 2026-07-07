from coding.Input import InputPlugin, FontVariance

from .FourCorner import FCCodeInfoEncoder, FCRadixParser

plugin = InputPlugin(
    method_name="fc",
    encoder_class=FCCodeInfoEncoder,
    radix_parser_class=FCRadixParser,
    font_variance=FontVariance.Traditional,
)
