

import Constant
from im.CodeInfo.DYCodeInfo import DYCodeInfo
from ..base.RadixManager import RadixManager
class DYRadixManager(RadixManager):
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

		strCodeList=infoDict.get(Constant.ATTRIB_CODE_EXPRESSION)

		codeList=None
		if strCodeList!=None:
			codeList=strCodeList.split(DYCodeInfo.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(DYCodeInfo.RADIX_SEPERATOR), codeList))

		codeInfo=DYCodeInfo(codeList)
		return codeInfo

