from gear.CodeInfo import CodeInfo

class DCCodeInfo(CodeInfo):
	def setRadixCodeProperties(self, propDict):
		self.actionList=[]

		description=propDict.get('資訊表示式', '')
		if len(description)>0 and description!='XXXX':
			actionList=description.split(',')
			self.actionList=actionList

	@property
	def characterCode(self):
		return self.getCharacterCode()

	def getCharacterCode(self):
		return ','.join(self.actionList)

