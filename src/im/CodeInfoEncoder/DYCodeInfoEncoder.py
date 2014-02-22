from ..CodeInfo.DYCodeInfo import DYCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class DYCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=DYCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getDYProp(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, operator, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLoong(self, codeInfo, operator, codeInfoList):
		"""運算 "龍" """

		dylist=list(map(lambda c: c.getDYProp(), codeInfoList))
		cat="".join(dylist)
		dy=cat[:3]+cat[-1] if len(cat)>4 else cat
		codeInfo.setDYProp(dy)

	def encodeAsEast(self, codeInfo, operator, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsEqual(self, codeInfo, operator, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

