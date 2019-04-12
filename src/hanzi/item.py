from injector import inject

class StructureTag:
	def __init__(self):
		self.codeInfoList=[]

		self.flagIsTemplateApplied = False
		self.flagIsSubstituteApplied = False
		self.flagIsCodeInfoGenerated = False

	def isTemplateApplied(self):
		return self.flagIsTemplateApplied

	def isSubstituteApplied(self):
		return self.flagIsSubstituteApplied

	def isCodeInfoGenerated(self):
		return self.flagIsCodeInfoGenerated

	def setTemplateApplied(self):
		self.flagIsTemplateApplied=True

	def setSubstituteApplied(self):
		self.flagIsSubstituteApplied=True

	def setCodeInfoList(self, codeInfoList):
		self.codeInfoList = codeInfoList
		self.flagIsCodeInfoGenerated = True

	def getCodeInfoList(self):
		return self.codeInfoList

	def getRadixCodeInfoList(self):
		return filter(lambda x: x.isSupportRadixCode(), self.codeInfoList)

