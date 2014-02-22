from ..CodeInfo.BSCodeInfo import BSCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class BSCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=BSCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getBSProp()[0], codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLoong(self, codeInfo, codeInfoList):
		"""運算 "龍" """

		bslist=list(map(lambda c: c.getBSProp()[0], codeInfoList))
		cat="".join(bslist)
		bs_incode=(cat[:3]+cat[-1]) if len(cat)>4 else cat
		bs_spcode=codeInfoList[-1].getBSProp()[1]
		codeInfo.setBSProp(bs_incode, bs_spcode)

	def encodeAsEast(self, codeInfo, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsEqual(self, codeInfo, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, codeInfoList)


	def encodeAsHan(self, codeInfo, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		self.encodeAsLoong(codeInfo, newCodeInfoList)

	def encodeAsYou(self, codeInfo, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		self.encodeAsLoong(codeInfo, newCodeInfoList)

