from .CJCodeInfo import CJCodeInfo
from .CJCodeInfoEncoder import CJCodeInfoEncoder
from ..base.RadixManager import RadixParser
from .CJLump import CJLump

import re
import sys

class CJRadixParser(RadixParser):
	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_SINGLETON_EXPRESSION='獨體表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		direction='*'
		description=infoDict.get(CJRadixParser.ATTRIB_CODE_EXPRESSION)
		description_singleton=infoDict.get(CJRadixParser.ATTRIB_SINGLETON_EXPRESSION)

		cjLumpList=self.parseCJLumpList(description)
		cjLumpList_singleton=self.parseCJLumpList(description_singleton)
		codeInfo=CJCodeInfo(direction, cjLumpList, cjLumpList_singleton)

		return codeInfo

	def parseCJLumpList(self, description):
		cjLumpList=[]

		if description!=None:
			description_list=description.split(",")
			for desc in description_list:
				matchResult=re.match("(\w*)(\[(\w*)\](\w*))?", desc)
				groups=matchResult.groups()
				frontCode=groups[0]
				tailingSurround=groups[2]
				rearCode=groups[3]
				if tailingSurround==None:
					tailingSurround=""

				matchResult=re.match("([A-Z]*)([a-z]*)", tailingSurround)
				groups=matchResult.groups()

				containerCode=groups[0]
				interiorCode=groups[1]

				cjLump=CJLump.generate(frontCode, containerCode, interiorCode)
				cjLumpList.append(cjLump)

		return cjLumpList

