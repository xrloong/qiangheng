from coding.Input import InputPlugin, FontVariance

from .DaYi import DYCodeInfoEncoder, DYRadixParser

plugin = InputPlugin(
    method_name="dy",
    encoder_class=DYCodeInfoEncoder,
    radix_parser_class=DYRadixParser,
    font_variance=FontVariance.Traditional,
)
