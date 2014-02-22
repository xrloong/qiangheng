import re
import sys

class Stroke:
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

		"挑捺",	# 例子：乀
		"橫捺",	# 例子：乁
		"圓",	# 例子：㔔
	]

	def __init__(self, description):
		matchResult=re.match("\((.*)\)(.*)", description)

		groups=matchResult.groups()
		strokeName=groups[0]
		self.name=strokeName
		if strokeName not in Stroke.STROKE_NAMES:
			print("不認得的筆畫名稱: %s"%strokeName, file=sys.stderr)

		strokeDescription=groups[1]

		descriptionList=strokeDescription.split(',')
		self.actionList=[StrokeAction(d) for d in descriptionList]

	def getName(self):
		return self.name

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
		self.action=int(description[0:4])
		self.x=int(description[4:6], 16)
		self.y=int(description[6:8], 16)

	def getCode(self):
		return "%04X%02X%02X"%(self.action, self.x, self.y)

	def scale(self, xScale, yScale):
		self.x=int(self.x*xScale)
		self.y=int(self.y*yScale)

	def translate(self, xOffset, yOffset):
		self.x=int(self.x+xOffset)
		self.y=int(self.y+yOffset)

