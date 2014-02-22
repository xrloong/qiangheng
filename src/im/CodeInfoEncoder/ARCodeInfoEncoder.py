from ..CodeInfo.ARCodeInfo import ARCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class ARCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=ARCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getARProp(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, operator, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLoong(self, codeInfo, operator, codeInfoList):
		"""運算 "龍" """

		arlist=list(map(lambda c: c.getARProp(), codeInfoList))
		cat="".join(arlist)
		ar=cat[:3]+cat[-1] if len(cat)>4 else cat
		codeInfo.setARProp(ar)

	def encodeAsEast(self, codeInfo, operator, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsEqual(self, codeInfo, operator, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

