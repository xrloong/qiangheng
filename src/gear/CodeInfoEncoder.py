
class CodeInfoEncoder:
	def __init__(self):
		pass

	def encode(self, codeInfo, operator, codeInfoList):
		for childCodeInfo in codeInfoList:
			codeVariance=childCodeInfo.getCodeVarianceType()
			codeInfo.codeVariance.multi(codeVariance)

		self.setByComps(codeInfo, operator, codeInfoList)

	def setByComps(self, codeInfo, operator, codeInfoList):
		codeInfo.setByComps(operator, codeInfoList)

