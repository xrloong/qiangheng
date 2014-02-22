
class CodeInfoManager:
	def __init__(self, radixManager):
		self.radixManager=radixManager
		self.codeInfoEncoder=radixManager.getEncoder()

	def loadRadix(self, radixFileList):
		return self.radixManager.loadRadix(radixFileList)

	def hasRadix(self, charName):
		return self.radixManager.hasRadix(charName)

	def getRadixCodeInfoList(self, charName):
		return self.radixManager.getRadixCodeInfoList(charName)


	def interpretCodeInfo(self, codeInfo):
		return codeInfo.toCode()

	def encodeToCodeInfo(self, operator, codeInfoList):
		codeInfo=self.codeInfoEncoder.setByComps(operator, codeInfoList)
		return codeInfo

