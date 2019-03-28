from injector import inject
from injector import singleton

from Constant import Package

@singleton
class CodeInfoManager:
	@inject
	def __init__(self, imPackage: Package):
		imName=imPackage.IMInfo.IMName
		codeInfoEncoder=imPackage.CodeInfoEncoder
		self.radixParser=imPackage.RadixParser(imName, codeInfoEncoder)
		self.codeInfoEncoder=imPackage.CodeInfoEncoder
		self.radixCodeInfoDB={}
		self.resetRadixList=[]


	def loadRadix(self, radixFileList):
		[self.resetRadixList, self.radixCodeInfoDB]=self.radixParser.loadRadix(radixFileList)

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)

	def hasResetRadix(self, radixName):
		return (radixName in self.resetRadixList)

	def getResetRadixList(self):
		return self.resetRadixList


	def interpretCodeInfo(self, codeInfo):
		return codeInfo.toCode()

	def encodeToCodeInfo(self, operator, codeInfoList):
		codeInfo=self.codeInfoEncoder.setByComps(operator, codeInfoList)
		return codeInfo

	def interpretCodeInfoList(self, codeInfoList):
		codeList=[]
		for codeInfo in codeInfoList:
			characterCode=self.interpretCodeInfo(codeInfo)
			variance=codeInfo.variance
			if characterCode:
				codeList.append([characterCode, variance])

		return codeList
