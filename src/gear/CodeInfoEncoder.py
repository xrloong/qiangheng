
class CodeInfoEncoder:
	def __init__(self):
		pass

	def encode(self, codeInfo, operator, codeInfoList):
		for childCodeInfo in codeInfoList:
			codeVariance=childCodeInfo.getCodeVarianceType()
			codeInfo.codeVariance.multi(codeVariance)

		codeInfo.setByComps(operator, codeInfoList)

