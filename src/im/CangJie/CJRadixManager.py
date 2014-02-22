from .CJCodeInfo import CJCodeInfo
from .CJCodeInfoEncoder import CJCodeInfoEncoder
from ..base.RadixManager import RadixParser
from .CJLump import CJLump

import re
import sys

class CJRadixParser(RadixParser):
	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_SINGLE_CODE='獨體編碼'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		direction='*'
		singleCode=infoDict.get(CJRadixParser.ATTRIB_SINGLE_CODE)
		rtlist=[]
		description=infoDict.get(CJRadixParser.ATTRIB_CODE_EXPRESSION)

		cjLumpList=self.parseCJLumpList(description)
		codeInfo=CJCodeInfo(singleCode, direction, cjLumpList)

		return codeInfo

	def parseCJLumpList(self, description):
		cjLumpList=[]

		if description!=None:
			matchResult=re.match("(\w*)(\[(\w*)\](\w*))?", description)
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

