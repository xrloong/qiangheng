from injector import inject

class StructureTag:
	def __init__(self):
		self.codeInfoList=[]

		self.flagIsTemplateApplied=False
		self.flagIsSubstituteApplied=False

	def isTemplateApplied(self):
		return self.flagIsTemplateApplied

	def isSubstituteApplied(self):
		return self.flagIsSubstituteApplied

	def setTemplateApplied(self):
		self.flagIsTemplateApplied=True

	def setSubstituteApplied(self):
		self.flagIsSubstituteApplied=True

	def setCodeInfoList(self, codeInfoList):
		self.codeInfoList=codeInfoList

	def getCodeInfoList(self):
		return self.codeInfoList

	def getRadixCodeInfoList(self):
		return filter(lambda x: x.isSupportRadixCode(), self.codeInfoList)

class StructureUnitTag(StructureTag):
	def __init__(self):
		super().__init__()

class StructureWrapperTag(StructureTag):
	def __init__(self):
		super().__init__()

class StructureCompoundTag(StructureTag):
	def __init__(self):
		super().__init__()

