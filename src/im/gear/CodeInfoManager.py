
class CodeInfoManager:
	def __init__(self, radixParser, codeInfoEncoder):
		self.radixParser=radixParser
		self.codeInfoEncoder=codeInfoEncoder
		self.radixCodeInfoDB={}


	def loadRadix(self, radixFileList):
		self.radixCodeInfoDB=self.radixParser.loadRadix(radixFileList)

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)


	def interpretCodeInfo(self, codeInfo):
		return codeInfo.toCode()

	def encodeToCodeInfo(self, operator, codeInfoList):
		codeInfo=self.codeInfoEncoder.setByComps(operator, codeInfoList)
		return codeInfo

