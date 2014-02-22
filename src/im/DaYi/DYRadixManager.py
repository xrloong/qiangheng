from .DYCodeInfo import DYCodeInfo
from .DYCodeInfoEncoder import DYCodeInfoEncoder
from ..base.RadixManager import RadixParser
import Constant

class DYRadixParser(RadixParser):
	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

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

