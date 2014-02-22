import re
import sys
from gear.CodeInfo import CodeInfo
from gear.Stroke import Stroke

class DCCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeList, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self.strokeList=strokeList

	@staticmethod
	def generateDefaultCodeInfo(strokeList):
		codeInfo=DCCodeInfo(strokeList)
		return codeInfo

	@staticmethod
	def generateCodeInfo(propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(propDict)
		strokeList=[]
		description=propDict.get('資訊表示式', '')
		if len(description)>0 and description!='XXXX':
			strokeDescriptionList=description.split(DCCodeInfo.STROKE_SEPERATOR)
			strokeList=[]
			for d in strokeDescriptionList:
				stroke=Stroke(d)
				strokeList.append(stroke)

		codeInfo=DCCodeInfo(strokeList, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	def toCode(self):
		return self.getCode()

	def getStrokeList(self):
		return self.strokeList

	def getCode(self):
		codeList=[stroke.getCode() for stroke in self.strokeList]
		return ','.join(codeList)

