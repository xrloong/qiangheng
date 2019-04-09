from injector import inject

class HanZiStructure:
	def __init__(self, tag):
		self.referenceNode=None
		self.index=0
		self.operator=None
		self.structureList=[]

		self.tag=tag

	def __str__(self):
		if self.isWrapper():
			tag=self.getTag()
			return str(self.tag)
		else:
			structureList=self.getStructureList()
			nameList=[str(structure) for structure in structureList]
			return "(%s %s)"%(self.getOperator(), " ".join(nameList))

	def isWrapper(self):
		return bool(self.referenceNode)

	def getUniqueName(self):
		strucutreExpression=""
		referenceExpression=""

		if self.operator:
			structureList=self.getStructureList()
			nameList=[structure.getUniqueName() for structure in structureList]
			strucutreExpression="%s %s"%(self.getOperator(), " ".join(nameList))

		if self.referenceNode:
			tag=self.getTag()
			referenceExpression=tag.getReferenceExpression()

		return "(%s|%s)"%(referenceExpression, strucutreExpression)

	def getReferenceNode(self):
		return self.referenceNode

	def getOperator(self):
		return self.operator

	def getOperatorName(self):
		if self.isWrapper():
			referenceNode=self.getReferenceNode()
			structure=referenceNode.getStructure()
			if structure:
				return structure.getOperator().getName()
			else:
				return ""
		else:
			return self.getOperator().getName()

	def getReferenceName(self):
		if self.isWrapper():
			return self.getReferenceNode().getName()
		else:
			return

	def getExpandedStructure(self):
		if self.isWrapper():
			expandedStructure=self.getReferenceNode().getStructure()
			if expandedStructure:
				return expandedStructure
			else:
				return self
		else:
			return self

	def getReferenceExpression(self):
		if self.isWrapper():
			tag=self.getTag()
			return tag.getReferenceExpression()
		else:
			return


	def getStructureList(self):
		if self.isWrapper():
			structure=self.referenceNode.getStructure()
			if structure:
				return [structure]
			else:
				return []
		return self.structureList

	def setAsCompound(self, operator, structureList):
		self.operator=operator
		self.structureList=structureList

	def setAsWrapper(self, referenceNode, index):
		self.referenceNode=referenceNode
		self.index=index

	def setNewStructure(self, newTargetStructure):
		self.setAsCompound(newTargetStructure.operator, newTargetStructure.structureList)

	def getTag(self):
		return self.tag

	def generateCodeInfos(self):
		def getAllWrapperStructureList():
			expression=self.getTag().getReferenceExpression()
			tempList=expression.split(".")
			if(len(tempList)>1):
				referenceName=tempList[0]
				index=int(tempList[1])-1
				structure=self.referenceNode.getSubStructure(index)
				structureList=[structure]
			else:
				structureList=self.referenceNode.getStructureList(True)
			return structureList

		def getTagList():
			if self.isWrapper():
				structureList=getAllWrapperStructureList()
			else:
				structureList=self.structureList

			return [structure.getTag() for structure in structureList]

		self.getTag().generateCodeInfos(self.getOperator(), getTagList())


class HanZiNode:
	def __init__(self, name, tag):
		self.name=name
		self.structure=None
		self.unitStructureList=[]
		self.tag=tag

	def __str__(self):
		return self.name

	def getName(self):
		return self.name

	def setStructure(self, structure):
		self.structure=structure

	def getStructure(self):
		return self.structure

	def getStructureList(self, isWithUnit=False):
		structureList=[]

		if self.structure:
			structureList=[self.structure]

		if isWithUnit:
			structureList.extend(self.unitStructureList)

		return structureList

	def addUnitStructure(self, structure):
		self.unitStructureList.append(structure)

	def getUnitStructureList(self):
		return self.unitStructureList

	def getSubStructure(self, index):
		structure=self.getStructure()
		if not structure:
			return None

		structureList=structure.getStructureList()
		return structureList[index]

	def getTag(self):
		return self.tag

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

	def printAllCodeInfo(self):
		for codeInfo in self.getCodeInfoList():
			pass

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

	def setInfoListList(self, operator, infoListList):
		codeInfoList=[]
		for infoList in infoListList:
			codeInfo = self.codeInfoInterpreter.encodeToCodeInfo(operator, infoList)
			if codeInfo!=None:
				for childCodeInfo in infoList:
					codeVariance=childCodeInfo.getCodeVarianceType()
					codeInfo.multiplyCodeVarianceType(codeVariance)

				codeInfoList.append(codeInfo)
		self.setCodeInfoList(codeInfoList)

	def generateCodeInfos(self, operator, tagList):
		infoListList=StructureAssemblageTag.getAllCodeInfoListFragTagList(tagList)
		self.setInfoListList(operator, infoListList)

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
			tmpCodeInfoList=tag.getCodeInfoList()
			codeInfoList=filter(lambda x: x.isSupportRadixCode(), tmpCodeInfoList)
			infoListList=combineList(infoListList, codeInfoList)

		return infoListList


