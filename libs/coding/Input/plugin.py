from pydantic import BaseModel, ConfigDict

from element.enum import FontVariance
from .Input import CodeMappingInfoInterpreter


class InputPlugin(BaseModel):
    """輸入法插件的合約與預設設定。

    框架所需的屬性（CodeInfoEncoder、CodingRadixParser、fontVariance、
    codeMappingInfoInterpreter、CodingSubstituteFileList、CodingRadixFileList、
    CodingAdjustFileList）全部由此類別提供，路徑由 method_name 自動推導；
    資料不在 gen/qhdata/ 下的插件（如 samples/）可用 method_dir 指定目錄。

    用法：
        plugin = InputPlugin(
            method_name="ar",
            encoder_class=ARCodeInfoEncoder,
            radix_parser_class=ARRadixParser,
            font_variance=FontVariance.Traditional,
        )
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    method_name: str
    encoder_class: type
    radix_parser_class: type
    font_variance: FontVariance = FontVariance.Traditional
    has_fast_file: bool = False
    method_dir: str | None = None

    @property
    def _method_dir(self) -> str:
        return self.method_dir or f"gen/qhdata/{self.method_name}/"

    # ── 框架所需屬性 ────────────────────────────────────────────────────────

    @property
    def CodeInfoEncoder(self) -> type:
        return self.encoder_class

    @property
    def CodingRadixParser(self) -> type:
        return self.radix_parser_class

    @property
    def fontVariance(self) -> FontVariance:
        return self.font_variance

    @property
    def codeMappingInfoInterpreter(self) -> CodeMappingInfoInterpreter:
        return CodeMappingInfoInterpreter()

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
    def CodingFastFile(self) -> str:
        if self.has_fast_file:
            return self._method_dir + "fast.yaml"
        raise AttributeError(f"{self.method_name!r} plugin has no fast file")
