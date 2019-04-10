from injector import inject

class StructureTag:
	def __init__(self):
		self.codeInfoList=[]

		self.flagIsCodeInfoGenerated=False
		self.flagIsTemplateApplied=False
		self.flagIsSubstituteApplied=False

	def isCodeInfoGenerated(self):
		return self.flagIsCodeInfoGenerated

	def isTemplateApplied(self):
		return self.flagIsTemplateApplied

	def isSubstituteApplied(self):
		return self.flagIsSubstituteApplied

	def setCodeInfoGenerated(self):
		self.flagIsCodeInfoGenerated=True

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

	def generateCodeInfos(self, operator, tagList):
		pass

class StructureUnitTag(StructureTag):
	def __init__(self, radixCodeInfo):
		super().__init__()
		self.codeInfoList=[radixCodeInfo]

	def __str__(self):
		return str(self.codeInfoList)

	def getCodeInfoList(self):
		return self.codeInfoList

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

	def getIndex(self):
		return self.index

	def getReferenceName(self):
		return self.referenceName

	def getReferenceExpression(self):
		return self.referenceExpression

	def generateCodeInfos(self, operator, tagList):
		codeInfoList=[]
		for tag in tagList:
			codeInfoList.extend(tag.getCodeInfoList())
		self.setCodeInfoList(codeInfoList)

class StructureAssemblageTag(StructureTag):
	def __init__(self, codeInfoInterpreter):
		super().__init__()
		self.codeInfoInterpreter = codeInfoInterpreter

	def generateCodeInfos(self, operator, tagList):
		infoListList=StructureAssemblageTag.getAllCodeInfoListFragTagList(tagList)
		codeInfoList=[]
		for infoList in infoListList:
			codeInfo = self.codeInfoInterpreter.encodeToCodeInfo(operator, infoList)
			if codeInfo!=None:
				for childCodeInfo in infoList:
					codeVariance=childCodeInfo.getCodeVarianceType()
					codeInfo.multiplyCodeVarianceType(codeVariance)

				codeInfoList.append(codeInfo)
		self.setCodeInfoList(codeInfoList)

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


