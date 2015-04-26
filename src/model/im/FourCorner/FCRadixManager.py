from .FCCodeInfo import FCCodeInfo
from .FCCodeInfoEncoder import FCCodeInfoEncoder
from model.base.RadixManager import RadixParser

class FCRadixParser(RadixParser):
	ATTRIB_CODE_EXPRESSION='資訊表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		top_left=''
		top_right=''
		bottom_left=''
		bottom_right=''

		characterCode=infoDict.get(FCRadixParser.ATTRIB_CODE_EXPRESSION)
		if len(characterCode)==4:
			top_left=characterCode[0]
			top_right=characterCode[1]
			bottom_left=characterCode[2]
			bottom_right=characterCode[3]

		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=FCCodeInfo(corners)
		return codeInfo

