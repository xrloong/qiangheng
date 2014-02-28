from .ARCodeInfo import ARCodeInfo
from .ARCodeInfoEncoder import ARCodeInfoEncoder
from ..base.RadixManager import RadixParserYAML

class ARRadixParser(RadixParserYAML):
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

		codeList=None

		str_rtlist=infoDict.get(ARRadixParser.ATTRIB_CODE_EXPRESSION)
		if str_rtlist!=None:
			codeList=str_rtlist.split(ARRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ARRadixParser.RADIX_SEPERATOR), codeList))

		codeInfo=ARCodeInfo(codeList)
		return codeInfo

