from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from model.element.CodeVarianceType import CodeVarianceType

class RadixCodeInfoModel(BaseModel):
	varianceString: Optional[str] = Field(alias = '類型', default = None)
	supportCharacterCode: Optional[str] = Field(
            alias = '字符碼', pattern = "是",
            default = None,
            )

	@property
	def variance(self):
		variance = CodeVarianceType.fromString(self.varianceString)
		return variance

	@property
	def __hasSupportCharacterCode(self):
		return bool(self.supportCharacterCode)

	@property
	def isSupportRadixCode(self):
		return not self.__hasSupportCharacterCode
