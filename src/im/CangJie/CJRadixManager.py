from .CJCodeInfo import CJCodeInfo
from .CJCodeInfoEncoder import CJCodeInfoEncoder
from ..base.RadixManager import RadixManager
from .CJLump import CJLump
import Constant

import re
import sys

class CJRadixManager(RadixManager):
	def __init__(self, nameInputMethod):
		RadixManager.__init__(self, nameInputMethod)

	def createEncoder(self):
		return CJCodeInfoEncoder()

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

		direction='*'
		singleCode=infoDict.get('獨體編碼')
		rtlist=[]
		description=infoDict.get('資訊表示式')

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
