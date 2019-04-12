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
	def __init__(self, radixCodeInfo):
		super().__init__()
		self.radixCodeInfo = radixCodeInfo

	def __str__(self):
		return str(self.radixCodeInfo)

class StructureWrapperTag(StructureTag):
	def __init__(self, name, index):
		super().__init__()
		if index==0:
			referenceExpression="%s"%name
		else:
			referenceExpression="%s.%d"%(name, index)

		self.referenceName=name
		self.index=index
		self.referenceExpression=referenceExpression

	def __str__(self):
		return self.getReferenceExpression()

	def getReferenceExpression(self):
		return self.referenceExpression

class StructureCompoundTag(StructureTag):
	def __init__(self):
		super().__init__()

	@staticmethod
	def getAllCodeInfoListFragTagList(tagList):
		def combineList(infoListList, infoListOfNode):
			if len(infoListList)==0:
				ansListList=[]
				for codeInfo in infoListOfNode:
					ansListList.append([codeInfo])
			else:
				ansListList=[]
				for infoList in infoListList:
					for codeInfo in infoListOfNode:
						ansListList.append(infoList+[codeInfo])

			return ansListList

		infoListList=[]

		for tag in tagList:
			codeInfoList=tag.getRadixCodeInfoList()
			infoListList=combineList(infoListList, codeInfoList)

		return infoListList


