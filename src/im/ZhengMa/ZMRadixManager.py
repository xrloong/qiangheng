from .ZMCodeInfo import ZMCodeInfo
from .ZMCodeInfoEncoder import ZMCodeInfoEncoder
from ..base.RadixManager import RadixParser

import Constant

class ZMRadixParser(RadixParser):
	def createEncoder(self):
		return ZMCodeInfoEncoder()

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

		extra_code=infoDict.get('補充資訊')
		strCodeList=infoDict.get('資訊表示式')

		zm_code=''
		zm_extra=extra_code
		zm_single=infoDict.get('獨體編碼')
		codeList=[]
		if strCodeList!=None:
			codeList=strCodeList.split(ZMCodeInfo.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ZMCodeInfo.RADIX_SEPERATOR), codeList))

		codeInfo=ZMCodeInfo(zm_single, codeList, zm_extra)
		return codeInfo

