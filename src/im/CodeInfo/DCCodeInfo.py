from gear.CodeInfo import CodeInfo

class DCCodeInfo(CodeInfo):
	def __init__(self, actionList, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self.actionList=actionList

	@property
	def characterCode(self):
		return self.getCharacterCode()

	def getCharacterCode(self):
		descriptionList=[a.getCode() for a in self.actionList]
		return ','.join(descriptionList)

	def getActionList(self):
		return self.actionList

	def setActionList(self, actionList):
		self.actionList=actionList

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

