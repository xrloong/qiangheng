from . import CodeMappingInfo
from model import StateManager

class CharacterInfo:
	def __init__(self, charName):
		self.name=charName

	def setCodeInfoList(self, codeInfoList):
		codeInfoList=filter(lambda x: x.isSupportCharacterCode(), codeInfoList)

		codeInfoManager=StateManager.getCodeInfoManager()
		codeList=[]
		for codeInfo in codeInfoList:
			characterCode=codeInfoManager.interpretCodeInfo(codeInfo)
			variance=codeInfo.variance
			if characterCode:
				codeList.append([characterCode, variance])

		self.codePropList=codeList

	def getCodeMappingInfoList(self):
		characterInfoList=[]
		for codeAndType in self.codePropList:
			code, variance=codeAndType
			characterInfo=CodeMappingInfo.CodeMappingInfo(self.name, code, variance)
			characterInfoList.append(characterInfo)
		self.characterInfoList=characterInfoList

		return self.characterInfoList
