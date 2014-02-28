from .ZMCodeInfo import ZMCodeInfo
from .ZMCodeInfoEncoder import ZMCodeInfoEncoder
from ..base.RadixManager import RadixParserYAML


class ZMRadixParser(RadixParserYAML):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_SUPPLEMENTARY_CODE='補充資訊'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		extra_code=infoDict.get(ZMRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		strCodeList=infoDict.get(ZMRadixParser.ATTRIB_CODE_EXPRESSION)

		zm_code=''
		zm_extra=extra_code
		codeList=[]
		if strCodeList!=None:
			codeList=strCodeList.split(ZMRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ZMRadixParser.RADIX_SEPERATOR), codeList))

		codeInfo=ZMCodeInfo(codeList, zm_extra)
		return codeInfo

