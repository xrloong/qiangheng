from . import CodeMappingInfo

class CharacterInfo:
	def __init__(self, charName):
		self.name = charName

	@property
	def character(self):
		return self.name

	def setCodeProps(self, codeProps):
		self.codeProps = codeProps

	@property
	def codeMappingInfos(self):
		characterInfos = []

		for codeAndType in self.codeProps:
			code, variance = codeAndType
			characterInfo = CodeMappingInfo.CodeMappingInfo(self.name, code, variance)
			characterInfos.append(characterInfo)

		return characterInfos

