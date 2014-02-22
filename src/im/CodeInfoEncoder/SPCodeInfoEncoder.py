from ..CodeInfo.SPCodeInfo import SPCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class SPCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=SPCodeInfo(propDict, codeVariance)
		return codeInfo

	def setByComps(self, codeInfo, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getCharacterCode(), codeInfoList))
		if isAllWithCode:
			codeInfo.setCharacterCode('YYYY')

