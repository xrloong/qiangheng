from ..base.CodeInfo import CodeInfo
from .CJLump import CJLump

import sys

class CJCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	RADIX_丨='$丨'
	RADIX_乚='$乚'
	RADIX_丨丨='$丨丨'
	RADIX_儿='$儿'

	radixToCodeDict={
		RADIX_丨:['*', ['l']],
		RADIX_乚:['*', ['u']],
		RADIX_丨丨:['-', ['l', 'l']],
		RADIX_儿:['-', ['h', 'u']],
	}

	def __init__(self, singleCode, direction, cjLumpList):
		CodeInfo.__init__(self)

		self.singleCode=singleCode
		self.direction=direction
		self.cjLumpList=cjLumpList

		self.specialRadix=None

	def setSpecialRadix(self, specialRadix):
		self.specialRadix=specialRadix

	def getSpecialRadix(self):
		return self.specialRadix

	@staticmethod
	def generateDefaultCodeInfo(direction, cjLumpList):
		codeInfo=CJCodeInfo(None, direction, cjLumpList)

		return codeInfo

	def toCode(self):
		singletonCode=self.getSingletonCode()
		if singletonCode:
			return singletonCode
		else:
			direction=self.getDirection()
			if direction=='$':
				rtlist=self.cjLumpList
				return CJLump.computeSingletonCode(rtlist)
			else:
				rtlist=self.cjLumpList
				return CJLump.computeTotalCode(rtlist)


	def getSingletonCode(self):
		return self.singleCode

	def getDirection(self):
		return self.direction

	def getLumpList(self):
		return self.cjLumpList

CJCodeInfo.CODE_INFO_丿=CJCodeInfo('', '*', [CJLump.generate("h", "", "")])
CJCodeInfo.CODE_INFO_乚=CJCodeInfo('', '*', [CJLump.generate("u", "", "")])
CJCodeInfo.CODE_INFO_丨=CJCodeInfo('', '*', [CJLump.generate("l", "", "")])

