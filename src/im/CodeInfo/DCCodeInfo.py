from gear.CodeInfo import CodeInfo

class DCCodeInfo(CodeInfo):
	def __init__(self, strokeList, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self.strokeList=strokeList

	def getStrokeList(self):
		return self.strokeList

	def getCode(self):
		codeList=[stroke.getCode() for stroke in self.strokeList]
		return ','.join(codeList)
		return ';'.join(codeList)

class Stroke:
	def __init__(self, description):
		descriptionList=description.split(',')
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

