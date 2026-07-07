from coding.Input import InputPlugin, FontVariance

from .ZhengMa import ZMCodeInfoEncoder, ZMRadixParser

plugin = InputPlugin(
    method_name="zm",
    encoder_class=ZMCodeInfoEncoder,
    radix_parser_class=ZMRadixParser,
    font_variance=FontVariance.Simplified,
    has_fast_file=True,
)
