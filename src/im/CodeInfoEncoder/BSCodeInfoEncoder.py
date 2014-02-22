from ..CodeInfo.BSCodeInfo import BSCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class BSCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=BSCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getBSProp()[0], codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, operator, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLoong(self, codeInfo, operator, codeInfoList):
		"""運算 "龍" """

		bslist=list(map(lambda c: c.getBSProp()[0], codeInfoList))
		cat="".join(bslist)
		bs_incode=(cat[:3]+cat[-1]) if len(cat)>4 else cat
		bs_spcode=codeInfoList[-1].getBSProp()[1]
		codeInfo.setBSProp(bs_incode, bs_spcode)

	def encodeAsEast(self, codeInfo, operator, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsEqual(self, codeInfo, operator, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

