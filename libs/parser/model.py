from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict

from model.element.CodeVariance import CodeVariance

class RadixCodeInfoModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	varianceString: Optional[str] = Field(alias = '類型', default = None)
	supportCharacterCode: Optional[str] = Field(
            alias = '字符碼', pattern = "是",
            default = None,
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

class SubstituteRuleModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	pattern: str = Field(alias = '比對')
	replacement: str = Field(alias = '替換')

class SubstituteRuleSetModel(BaseModel):
	model_config = ConfigDict(frozen = True)

	rules: list[SubstituteRuleModel] = Field(alias = '規則集')

