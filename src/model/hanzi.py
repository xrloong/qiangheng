from model import StateManager

class StructureTag:
	def __init__(self):
		self.codeInfoList=[]

		self.flagIsCodeInfoGenerated=False
		self.flagIsTemplateApplied=False
		self.flagIsSubstituteApplied=False

	def isUnit(self):
		return False

	def isWrapper(self):
		return False

	def isAssemblage(self):
		return False

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

	def getReferenceExpression(self):
		return None

	def generateCodeInfos(self, operator, tagList):
		pass

class StructureUnitTag(StructureTag):
	def __init__(self, radixCodeInfo):
		super().__init__()
		self.codeInfoList=[radixCodeInfo]

	def __str__(self):
		return str(self.codeInfoList)

	def isUnit(self):
		return True

	def getCodeInfoList(self):
		return self.codeInfoList

class StructureWrapperTag(StructureTag):
	def __init__(self, referenceExpression):
		super().__init__()
		self.referenceExpression=referenceExpression

	def __str__(self):
		return self.getReferenceExpression()

	def isWrapper(self):
		return True

	def getReferenceExpression(self):
		return self.referenceExpression

	def generateCodeInfos(self, operator, tagList):
		codeInfoList=[]
		for tag in tagList:
			codeInfoList.extend(tag.getCodeInfoList())
		self.setCodeInfoList(codeInfoList)

class StructureAssemblageTag(StructureTag):
	def __init__(self):
		super().__init__()

	def isAssemblage(self):
		return True

	def setInfoListList(self, operator, infoListList):
		codeInfoManager=StateManager.getCodeInfoManager()
		codeInfoList=[]
		for infoList in infoListList:
			codeInfo=codeInfoManager.encodeToCodeInfo(operator, infoList)
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

class HanZiStructure:
	def __init__(self, tag):
		self.referenceNode=None
		self.operator=None
		self.structureList=[]

		self.tag=tag

	def __str__(self):
		if self.isAssemblage():
			structureList=self.getStructureList()
			nameList=[structure.getUniqueName() for structure in structureList]
			return "(%s %s)"%(self.getOperator().getName(), " ".join(nameList))
		return str(self.tag)

	def getUniqueName(self):
		if self.isWrapper():
			return self.getTag().getReferenceExpression()
		elif self.isAssemblage():
			structureList=self.getStructureList()
			nameList=[structure.getUniqueName() for structure in structureList]
			return "(%s %s)"%(self.getOperator().getName(), " ".join(nameList))

	def isUnit(self):
		return self.tag.isUnit()

	def isWrapper(self):
		return self.tag.isWrapper()

	def isAssemblage(self):
		return self.tag.isAssemblage()

	def getOperator(self):
		return self.operator

	def getStructureList(self):
		if self.referenceNode:
			return self.getWrapperStructureList()
		return self.structureList

	def getWrapperStructureList(self):
		expression=self.getTag().getReferenceExpression()
		tempList=expression.split(".")
		if(len(tempList)>1):
			referenceName=tempList[0]
			index=int(tempList[1])
			structureList=self.referenceNode.getSubStructureList(index)
		else:
			structureList=self.referenceNode.getStructureList()
		return structureList

	def setAsCompound(self, operator, structureList):
		self.operator=operator
		self.structureList=structureList

	def setAsWrapper(self, referenceNode):
		self.referenceNode=referenceNode

	def setNewStructure(self, newTargetStructure):
		self.setAsCompound(newTargetStructure.operator, newTargetStructure.structureList)

	def getTag(self):
		return self.tag

	def getTagList(self):
		return [structure.getTag() for structure in self.getStructureList()]

	def generateCodeInfos(self):
		self.getTag().generateCodeInfos(self.getOperator(), self.getTagList())


class HanZiNode:
	def __init__(self, name, tag):
		self.name=name
		self.structureList=[]
		self.tag=tag

	def getName(self):
		return self.name

	def addStructure(self, structure):
		self.structureList.append(structure)

	def setStructureList(self, structureList):
		self.structureList=structureList

	def getStructureList(self):
		return self.structureList

	def getSubStructureList(self, index):
		subStructureList=[]
		for structure in self.structureList:
			structureList=structure.getStructureList()
			subStructureList.append(structureList[index])
		return subStructureList

	def getTag(self):
		return self.tag

class HanZiNetwork:
	def __init__(self):
		self.nodeDict={}
		self.structureDict={}

		self.nodeExpressionDict={}

	def addNode(self, name, tag):
		if name not in self.nodeDict:
			node=HanZiNode(name, tag)
			self.nodeDict[name]=node

	def addStructure(self, structureName, structure):
		self.structureDict[structureName]=structure

	def addStructureIntoNode(self, structure, nodeName):
		dstNode=self.findNode(nodeName)
		dstNode.addStructure(structure)

	def findNode(self, nodeName):
		return self.nodeDict.get(nodeName)

	def generateOperator(self, operatorName):
		operator=StateManager.getOperationManager().generateOperator(operatorName)
		return operator

	def generateAssemblageStructure(self, operator, structureList):
		tag=StructureAssemblageTag()
		structure=HanZiStructure(tag)
		structure.setAsCompound(operator, structureList)
		return structure

	def generateWrapperStructure(self, name, nodeExpression):
		if nodeExpression in self.nodeExpressionDict:
			return self.nodeExpressionDict[nodeExpression]
		rootNode=self.findNode(name)

		tag=StructureWrapperTag(nodeExpression)
		structure=HanZiStructure(tag)
		structure.setAsWrapper(rootNode)

		self.nodeExpressionDict[nodeExpression]=structure
		return structure

	def generateUnitStructure(self, radixCodeInfo):
		tag=StructureUnitTag(radixCodeInfo)
		structure=HanZiStructure(tag)
		return structure

