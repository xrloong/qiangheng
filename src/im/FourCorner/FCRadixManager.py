from .FCCodeInfo import FCCodeInfo
from .FCCodeInfoEncoder import FCCodeInfoEncoder
from ..base.RadixManager import RadixParser

import Constant

class FCRadixParser(RadixParser):
	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		top_left=''
		top_right=''
		bottom_left=''
		bottom_right=''

		characterCode=infoDict.get('資訊表示式', '')
		if len(characterCode)==4:
			top_left=characterCode[0]
			top_right=characterCode[1]
			bottom_left=characterCode[2]
			bottom_right=characterCode[3]

		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=FCCodeInfo(corners)
		return codeInfo

