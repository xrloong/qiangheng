from coding.Input import InputPlugin, FontVariance

from .Boshiamy import BSCodeInfoEncoder, BSRadixParser

plugin = InputPlugin(
    method_name="bs",
    encoder_class=BSCodeInfoEncoder,
    radix_parser_class=BSRadixParser,
    font_variance=FontVariance.Traditional,
    has_fast_file=True,
)
