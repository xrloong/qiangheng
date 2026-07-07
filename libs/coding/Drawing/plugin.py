import functools
from dataclasses import dataclass

from element.enum import FontVariance
from .Drawing import CodeMappingInfoInterpreter


@dataclass
class DrawingPlugin:
    """描繪法插件的合約與預設設定。

    與 InputPlugin 的主要差異：
    - codeMappingInfoInterpreter 由外部傳入（描繪法通常有自訂的 interpreter）
    - 固定提供 CodingTemplateFile（描繪法需要筆劃模板）

    用法：
        plugin = DrawingPlugin(
            method_name="dc",
            encoder_class=DCCodeInfoEncoder,
            radix_parser_class=DCRadixParser,
            interpreter=DCCodeMappingInfoInterpreter(),
        )
    """

    method_name: str
    encoder_class: type
    radix_parser_class: type
    interpreter: CodeMappingInfoInterpreter
    font_variance: FontVariance = FontVariance.Traditional

    @property
    def _method_dir(self) -> str:
        return f"gen/qhdata/{self.method_name}/"

    # ── 框架所需屬性 ────────────────────────────────────────────────────────

    @property
    def CodeInfoEncoder(self) -> type:
        return self.encoder_class

    @property
    def CodingRadixParser(self):
        return functools.partial(self.radix_parser_class, self.CodingTemplateFile)

    @property
    def fontVariance(self) -> FontVariance:
        return self.font_variance

    @property
    def codeMappingInfoInterpreter(self) -> CodeMappingInfoInterpreter:
        return self.interpreter

    @property
    def CodingSubstituteFileList(self) -> list[str]:
        return [self._method_dir + "substitute.yaml"]

    @property
    def CodingRadixFileList(self) -> list[str]:
        return [
            self._method_dir + "radix/CJK.yaml",
            self._method_dir + "radix/CJK-A.yaml",
        ]

    @property
    def CodingAdjustFileList(self) -> list[str]:
        return [self._method_dir + "adjust.yaml"]

    @property
    def CodingTemplateFile(self) -> str:
        return self._method_dir + "radix/template.yaml"
