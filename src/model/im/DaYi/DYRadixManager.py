from .DYCodeInfo import DYCodeInfo
from .DYCodeInfoEncoder import DYCodeInfoEncoder
from model.base.RadixManager import RadixParser

class DYRadixParser(RadixParser):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='資訊表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		strCodeList=infoDict.get(DYRadixParser.ATTRIB_CODE_EXPRESSION)

		codeList=None
		if strCodeList!=None:
			codeList=strCodeList.split(DYRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(DYRadixParser.RADIX_SEPERATOR), codeList))

		codeInfo=DYCodeInfo(codeList)
		return codeInfo

