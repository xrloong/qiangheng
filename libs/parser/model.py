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

class SubstituteRuleModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	pattern: str = Field(alias = '比對', frozen = True)
	replacement: str = Field(alias = '替換', frozen = True)

class SubstituteRuleSetModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	rules: list[SubstituteRuleModel] = Field(alias = '規則集', frozen = True)

