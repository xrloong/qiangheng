from .BSCodeInfo import BSCodeInfo
from .BSCodeInfoEncoder import BSCodeInfoEncoder
from ..base.RadixManager import RadixParser

class BSRadixParser(RadixParser):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_DIGITAL='基本數字'
	ATTRIB_SUPPLEMENTARY_CODE='嘸蝦米補碼'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		strCodeList=infoDict.get(BSRadixParser.ATTRIB_CODE_EXPRESSION)
		supplementCode=infoDict.get(BSRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		isDigital=True if infoDict.get(BSRadixParser.ATTRIB_DIGITAL) != None else False

		codeList=None
		if strCodeList!=None:
			codeList=strCodeList.split(BSRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(BSRadixParser.RADIX_SEPERATOR), codeList))

		codeInfo=BSCodeInfo(codeList, supplementCode, isDigital)
		return codeInfo


