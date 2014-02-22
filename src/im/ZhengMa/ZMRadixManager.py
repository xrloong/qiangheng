from .ZMCodeInfo import ZMCodeInfo
from .ZMCodeInfoEncoder import ZMCodeInfoEncoder
from ..base.RadixManager import RadixParser


class ZMRadixParser(RadixParser):
	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_SINGLE_CODE='獨體編碼'
	ATTRIB_SUPPLEMENTARY_CODE='補充資訊'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		extra_code=infoDict.get(ZMRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		strCodeList=infoDict.get(ZMRadixParser.ATTRIB_CODE_EXPRESSION)

		zm_code=''
		zm_extra=extra_code
		zm_single=infoDict.get(ZMRadixParser.ATTRIB_SINGLE_CODE)
		codeList=[]
		if strCodeList!=None:
			codeList=strCodeList.split(ZMCodeInfo.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ZMCodeInfo.RADIX_SEPERATOR), codeList))

		codeInfo=ZMCodeInfo(zm_single, codeList, zm_extra)
		return codeInfo

