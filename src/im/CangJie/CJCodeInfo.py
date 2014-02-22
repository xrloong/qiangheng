from ..base.CodeInfo import CodeInfo
from .CJLump import CJLump

import sys

class CJCodeInfo(CodeInfo):
	def __init__(self, singleCode, direction, cjLumpList):
		super().__init__()

		self.singleCode=singleCode
		self.direction=direction
		self.cjLumpList=cjLumpList

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

