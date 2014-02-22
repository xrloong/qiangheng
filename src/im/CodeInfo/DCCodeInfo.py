import re
import sys
from gear.CodeInfo import CodeInfo

class DCCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	STROKE_NAMES=[
		"XXXX",

		"點", "長頓點",

		"橫", "橫鉤", "橫折", "橫折橫",
		"橫折鉤", "橫撇", "橫曲鉤",
		"橫撇橫折鉤", "橫斜鉤",
		"橫折橫折",

		"豎", "豎折", "豎挑", "豎橫折",
		"豎橫折鉤", "豎曲鉤", "豎鉤",
		"臥鉤", "斜鉤", "彎鉤",

		"撇", "撇頓點", "撇橫", "撇挑",
		"撇折", "豎撇", "挑", "挑折",
		"捺",
	]

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

class Stroke:
	def __init__(self, description):
		matchResult=re.match("\((.*)\)(.*)", description)

		groups=matchResult.groups()
		strokeName=groups[0]
		if strokeName not in DCCodeInfo.STROKE_NAMES:
			print("不認得的筆畫名稱: %s"%strokeName, file=sys.stderr)

		strokeDescription=groups[1]

		descriptionList=strokeDescription.split(',')
		self.actionList=[StrokeAction(d) for d in descriptionList]

	def getActionList(self):
		return self.actionList

	def getCode(self):
		codeList=[x.getCode() for x in self.actionList]
		return ','.join(codeList)

	def scale(self, xScale, yScale):
		for action in self.actionList:
			action.scale(xScale, yScale)

	def translate(self, xOffset, yOffset):
		for action in self.actionList:
			action.translate(xOffset, yOffset)

class StrokeAction:
	def __init__(self, description):
		self.action=description[0:4]
		self.x=int(description[4:6], 16)
		self.y=int(description[6:8], 16)

	def getCode(self):
		return "%s%02X%02X"%(self.action, self.x, self.y)

	def scale(self, xScale, yScale):
		self.x=int(self.x*xScale)
		self.y=int(self.y*yScale)

	def translate(self, xOffset, yOffset):
		self.x=int(self.x+xOffset)
		self.y=int(self.y+yOffset)

