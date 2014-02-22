from .CodeInfo import CodeInfo

class CodeInfoEncoder:
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=CodeInfo(propDict, codeVariance)
		return codeInfo

	def encode(self, codeInfo, operator, codeInfoList):
		for childCodeInfo in codeInfoList:
			codeVariance=childCodeInfo.getCodeVarianceType()
			codeInfo.multiplyCodeVarianceType(codeVariance)

		self.setByComps(codeInfo, operator, codeInfoList)

	def setByComps(self, codeInfo, operator, codeInfoList):
		pass

