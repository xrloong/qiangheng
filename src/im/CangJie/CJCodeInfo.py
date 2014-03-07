from ..base.CodeInfo import CodeInfo
from .CJLump import CJLump

import sys

class CJCodeInfo(CodeInfo):
	def __init__(self, direction, cjLumpList, cjLumpListSingleton):
		super().__init__()

		self.direction=direction
		self.cjLumpList=cjLumpList
		self.cjLumpListSingleton=cjLumpListSingleton

	@staticmethod
	def generateDefaultCodeInfo(direction, cjLumpList):
		codeInfo=CJCodeInfo(direction, cjLumpList, None)

		return codeInfo

	def toCode(self):
		direction=self.getDirection()

		if self.cjLumpListSingleton:
			rtlist=self.cjLumpList
			rtlist=self.cjLumpListSingleton
			return CJLump.computeTotalCode(rtlist)
		else:
			rtlist=self.cjLumpList
			if direction=='$':
				return CJLump.computeSingletonCode(rtlist)
			else:
				return CJLump.computeTotalCode(rtlist)


	def getDirection(self):
		return self.direction

	def getLumpList(self):
		return self.cjLumpList

class GridCJCodeInfo(CJCodeInfo):
	def __init__(self, codeInfoV, codeInfoH):
		CodeInfo.__init__(self)
#		super().__init__(codeInfoV.getDirection, codeInfoV.getLumpList, None)
		self.codeInfoV=codeInfoV
		self.codeInfoH=codeInfoH

	def toCode(self):
		return self.codeInfoV.toCode()

	def getDirection(self):
		return '+'

	def getLumpList(self):
		return self.codeInfoV.getLumpList()

	def getCodeInfoH(self):
		return self.codeInfoH

	def getCodeInfoV(self):
		return self.codeInfoV

