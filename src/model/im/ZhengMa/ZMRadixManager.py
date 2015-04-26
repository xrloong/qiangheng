from .ZMCodeInfo import ZMCodeInfo
from .ZMCodeInfoEncoder import ZMCodeInfoEncoder
from model.base.RadixManager import RadixParser


class ZMRadixParser(RadixParser):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_SUPPLEMENTARY_CODE='補充資訊'
	ATTRIB_SINGLETON_EXPRESSION='獨體表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		extra_code=infoDict.get(ZMRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		strCodeList=infoDict.get(ZMRadixParser.ATTRIB_CODE_EXPRESSION)
		strCodeListSingleton=infoDict.get(ZMRadixParser.ATTRIB_SINGLETON_EXPRESSION)

		zm_code=''
		zm_extra=extra_code
		codeList=[]
		if strCodeList!=None:
			codeList=strCodeList.split(ZMRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ZMRadixParser.RADIX_SEPERATOR), codeList))

		codeListSingleton=[]
		if strCodeListSingleton!=None:
			codeListSingleton=strCodeListSingleton.split(ZMRadixParser.INSTALLMENT_SEPERATOR)
			codeListSingleton=list(map(lambda x: x.split(ZMRadixParser.RADIX_SEPERATOR), codeListSingleton))

		codeInfo=ZMCodeInfo(codeList, zm_extra, codeListSingleton)
		return codeInfo

