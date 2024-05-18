from . import CodeMappingInfo
from .CodeVarianceType import CodeVarianceType
from model.element.CodeVarianceType import CodeVarianceTypeFactory

class CharacterInfo:
	def __init__(self, charName):
		self.name = charName
		self.fastCodeInfo = None

	@property
	def character(self):
		return self.name

	def setCodeProps(self, codeProps):
		self.codeProps = codeProps

	def setFastCode(self, code):
		varianceType = CodeVarianceTypeFactory.generate(codeVarianceType=CodeVarianceType.CODE_TYPE_SIMPLIFIED)
		variance = varianceType.getVarianceByString()
		self.fastCodeInfo = CodeMappingInfo.CodeMappingInfo(self.name, code, variance)

	@property
	def codeMappingInfos(self):
		characterInfos = []

		for codeAndType in self.codeProps:
			code, variance = codeAndType
			characterInfo = CodeMappingInfo.CodeMappingInfo(self.name, code, variance)
			characterInfos.append(characterInfo)
		if self.fastCodeInfo:
			characterInfos.append(self.fastCodeInfo)

		return characterInfos

