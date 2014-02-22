

import Constant
from im.CodeInfo.BSCodeInfo import BSCodeInfo
from gear.RadixManager import RadixManager
class BSRadixManager(RadixManager):
	def __init__(self, codeInfoEncoder):
		RadixManager.__init__(self, codeInfoEncoder)

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)

		self.setCodeInfoAttribute(codeInfo, radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		singletonCode=infoDict.get('獨體編碼')
		strCodeList=infoDict.get('資訊表示式')
		supplementCode=infoDict.get('嘸蝦米補碼')

		codeList=None
		if strCodeList!=None:
			codeList=strCodeList.split(BSCodeInfo.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(BSCodeInfo.RADIX_SEPERATOR), codeList))

		codeInfo=BSCodeInfo(singletonCode, codeList, supplementCode)
		return codeInfo


