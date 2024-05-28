from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict

from model.element.CodeVariance import CodeVariance

class RadixCodeInfoModel(BaseModel):
	model_config = ConfigDict(frozen = True, extra = 'allow')

	varianceString: Optional[str] = Field(alias = '類型', frozen = True, default = None)
	supportCharacterCode: Optional[str] = Field(
            alias = '字符碼', pattern = "是",
            frozen = True, default = None,
            )

	@property
	def variance(self):
		variance = CodeVariance.fromString(self.varianceString)
		return variance

	@property
	def __hasSupportCharacterCode(self):
		return bool(self.supportCharacterCode)

	@property
	def isSupportRadixCode(self):
		return not self.__hasSupportCharacterCode

class RadicalModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	name: str = Field(alias = '名稱', frozen = True)
	comment: str = Field(alias = '註記', frozen = True)
	codings: list[RadixCodeInfoModel] = Field(alias = '編碼資訊', frozen = True)

class RadicalSetModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	radicals: list[RadicalModel] = Field(alias = '字符集', frozen = True)

class SubstituteRuleMatchingModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	operator: str = Field(alias = '運算', frozen = True, default = None)
	operandCount: int = Field(alias = '參數個數', frozen = True)

class SubstituteRuleModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	matching: str | SubstituteRuleMatchingModel = Field(alias = '比對', frozen = True, default = None)
	replacement: str = Field(alias = '替換', frozen = True)

	templateName: Optional[str] = Field(alias = '範本名稱', frozen = True, default = None)
	parameterCount: Optional[int] = Field(alias = '參數個數', frozen = True, default = None)

class SubstituteRuleSetModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	rules: list[SubstituteRuleModel] = Field(alias = '規則集', frozen = True)

class StructureModel(BaseModel):
	model_config = ConfigDict(frozen = True, extra = 'allow')

	expression: str = Field(alias = '結構', frozen = True)
	font: Optional[str] = Field(
        alias = '字體', pattern = "傳|簡",
        frozen = True, default = None
    )

class CharacterDecompositionModel(BaseModel):
	model_config = ConfigDict(frozen = True, extra = 'allow')

	name: str = Field(alias = '名稱', frozen = True)
	comment: str = Field(alias = '註記', frozen = True)
	structureSet: list[StructureModel] = Field(alias = '結構集', frozen = True)

