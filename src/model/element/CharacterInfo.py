from . import CodeMappingInfo

from parser import constant

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
		variance = constant.VALUE_CODE_VARIANCE_TYPE_SIMPLIFIED
		self.fastCodeInfo = CodeMappingInfo.CodeMappingInfo(self.name, code, variance)

	@property
	def codeMappingInfos(self):
		characterInfos = []

		for codeAndVariance in self.codeProps:
			code, variance = codeAndVariance
			characterInfo = CodeMappingInfo.CodeMappingInfo(self.name, code, variance)
			characterInfos.append(characterInfo)
		if self.fastCodeInfo:
			characterInfos.append(self.fastCodeInfo)

		return characterInfos

