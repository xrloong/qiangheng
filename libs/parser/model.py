from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from element.enum import CodeVariance
from element.enum import FontVariance


class RadixCodeInfoModel(
    BaseModel,
    strict=True,
    frozen=True,
    extra="allow",
):
    variance: CodeVariance = Field(
        alias="類型", strict=False, default=CodeVariance.STANDARD
    )
    supportCharacterCode: Optional[str] = Field(
        alias="字符碼",
        pattern="是",
        default=None,
    )

    @field_validator("variance")
    @classmethod
    def __check_variance(cls, value):
        if value not in {CodeVariance.STANDARD, CodeVariance.TOLERANT}:
            raise ValueError("類型 應使用 標準|容錯")
        return value

    @property
    def __hasSupportCharacterCode(self):
        return bool(self.supportCharacterCode)

    @property
    def isSupportRadixCode(self):
        return not self.__hasSupportCharacterCode


class RadicalModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    name: str = Field(alias="名稱")
    comment: str = Field(alias="註記")
    codings: list[RadixCodeInfoModel] = Field(alias="編碼資訊")


class RadicalSetModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    radicals: list[RadicalModel] = Field(alias="字符集")


class SubstituteRuleMatchingModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    operator: Optional[str] = Field(alias="運算", default=None)
    operandCount: int = Field(alias="參數個數")


class SubstituteRuleModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    matching: str | SubstituteRuleMatchingModel | None = Field(
        alias="比對", default=None
    )
    replacement: str = Field(alias="替換")

    templateName: Optional[str] = Field(alias="範本名稱", default=None)
    parameterCount: Optional[int] = Field(alias="參數個數", default=None)


class SubstituteRuleSetModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    rules: list[SubstituteRuleModel] = Field(alias="規則集")


class StructureModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    expression: str = Field(alias="結構")
    font: FontVariance = Field(
        alias="字體", strict=False, default=FontVariance.All
    )

    @field_validator("font")
    @classmethod
    def __check_font(cls, value):
        if value not in {FontVariance.Traditional, FontVariance.Simplified}:
            raise ValueError("字體 應使用 傳|簡")
        return value


class CharacterDecompositionModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    name: str = Field(alias="名稱")
    comment: str = Field(alias="註記")
    structureSet: list[StructureModel] = Field(alias="結構集")


class CharacterDecompositionSetModel(
    BaseModel,
    strict=True,
    frozen=True,
):
    decompositionSet: list[CharacterDecompositionModel] = Field(
        alias="字符集"
    )
