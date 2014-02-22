from . import CodeMappingInfo

class CharacterInfo:
	def __init__(self, charName, freq):
		self.name=charName
		self.freq=freq

	def setCodeInfoList(self, codeInfoList):
		codeInfoList=filter(lambda x: x.isSupportCharacterCode(), codeInfoList)

		codeList=[]
		for codeInfo in codeInfoList:
			codeProp=codeInfo.getCodeProperties()
			if codeProp:
				codeList.append(codeProp)

		self.codePropList=codeList

	def getCodeMappingInfoList(self):
		characterInfoList=[]
		for codeAndType in self.codePropList:
			code, variance=codeAndType
			characterInfo=CodeMappingInfo.CodeMappingInfo(self.name, code, self.freq, variance)
			characterInfoList.append(characterInfo)
		self.characterInfoList=characterInfoList

		return self.characterInfoList

