import re
import sys
from gear.CodeInfo import CodeInfo

class DCCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeList):
		CodeInfo.__init__(self)

		self.strokeList=strokeList

	@staticmethod
	def generateDefaultCodeInfo(strokeList):
		codeInfo=DCCodeInfo(strokeList)
		return codeInfo

	def toCode(self):
		return self.getCode()

	def getStrokeList(self):
		return self.strokeList

	def getCode(self):
		codeList=[stroke.getCode() for stroke in self.strokeList]
		return ','.join(codeList)

