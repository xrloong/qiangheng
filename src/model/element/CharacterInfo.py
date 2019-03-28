from . import CodeMappingInfo

class CharacterInfo:
	def __init__(self, charName):
		self.name=charName

	def setCodeList(self, codeList):
		self.codePropList=codeList

	def getCodeMappingInfoList(self):
		characterInfoList=[]
		for codeAndType in self.codePropList:
			code, variance=codeAndType
			characterInfo=CodeMappingInfo.CodeMappingInfo(self.name, code, variance)
			characterInfoList.append(characterInfo)
		self.characterInfoList=characterInfoList

		return self.characterInfoList

