from ..CodeInfo.FCCodeInfo import FCCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class FCCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=FCCodeInfo(propDict, codeVariance)
		return codeInfo

	def setByComps(self, codeInfo, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getCharacterCode(), codeInfoList))
		if isAllWithCode:
			codeInfo.setCharacterCode('ZZZZ')

