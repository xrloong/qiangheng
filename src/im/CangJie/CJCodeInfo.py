from ..base.CodeInfo import CodeInfo
from .CJLump import CJLump

import sys

class CJCodeInfo(CodeInfo):
	def __init__(self, direction, cjLumpList):
		super().__init__()

		self.direction=direction
		self.cjLumpList=cjLumpList

	@staticmethod
	def generateDefaultCodeInfo(direction, cjLumpList):
		codeInfo=CJCodeInfo(direction, cjLumpList)

		return codeInfo

	def toCode(self):
		direction=self.getDirection()
		if direction=='$':
			rtlist=self.cjLumpList
			return CJLump.computeSingletonCode(rtlist)
		else:
			rtlist=self.cjLumpList
			return CJLump.computeTotalCode(rtlist)


	def getDirection(self):
		return self.direction

	def getLumpList(self):
		return self.cjLumpList

