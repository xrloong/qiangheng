from model import StateManager
from model.element import CharacterInfo

class HanZiStructure:
	def __init__(self):
		self.flagIsSet=False
		self.flagTemplateIsDone=False
		self.flagSubstituteIsDone=False

	def getUniqueName(self):
		if self.isWrapper():
			return self.getReferenceExpression()
		elif self.isAssemblage():
			structureList=self.getStructureList()
			nameList=[structure.getUniqueName() for structure in structureList]
			return "(%s %s)"%(self.getOperator().getName(), " ".join(nameList))

	def getReferenceExpression(self):
		return None

	def getOperator(self):
		return None

	def isUnit(self):
		return False

	def isWrapper(self):
		return False

	def isAssemblage(self):
		return False

	def getCodeInfoList(self):
		return []

	def getStructureList(self):
		return []

	def setCompositions(self):
		pass

	def printAllCodeInfo(self):
		for codeInfo in self.getCodeInfoList():
			pass

	def setTemplateDone(self):
		self.flagTemplateIsDone=True

	def setSubstituteDone(self):
		self.flagSubstituteIsDone=True

	def isTemplateDone(self):
		return self.flagTemplateIsDone

	def isSubstituteDone(self):
		return self.flagSubstituteIsDone

	@staticmethod
	def generateAssemblage(operator, structureList):
		structure=HanZiAssemblageStructure(operator, structureList)
		structure=HanZiProxyStructure(structure)
		return structure

	@staticmethod
	def generateWrapper(referenceNode, expression):
		structure=HanZiWrapperStructure(referenceNode, expression)
		structure=HanZiProxyStructure(structure)
		return structure

	@staticmethod
	def generateUnit(radixCodeInfo):
		structure=HanZiUnitStructure(radixCodeInfo)
		structure=HanZiProxyStructure(structure)
		return structure


class HanZiProxyStructure(HanZiStructure):
	def __init__(self, targetStructure):
		super().__init__()
		self.targetStructure=targetStructure
		self.historyStructures=[]

	def __str__(self):
		return str(self.targetStructure)

	def setNewStructure(self, newTargetStructure):
		self.historyStructures.append(self.targetStructure)
		self.targetStructure=newTargetStructure

	def getReferenceExpression(self):
		return self.targetStructure.getReferenceExpression()

	def getOperator(self):
		return self.targetStructure.getOperator()

	def isUnit(self):
		return self.targetStructure.isUnit()

	def isWrapper(self):
		return self.targetStructure.isWrapper()

	def isAssemblage(self):
		return self.targetStructure.isAssemblage()

	def getCodeInfoList(self):
		return self.targetStructure.getCodeInfoList()

	def getStructureList(self):
		return self.targetStructure.getStructureList()

	def setCompositions(self):
		self.targetStructure.setCompositions()

class HanZiUnitStructure(HanZiStructure):
	def __init__(self, radixCodeInfo):
		super().__init__()
		self.codeInfoList=[radixCodeInfo]

	def __str__(self):
		return str(self.codeInfoList)

	def isUnit(self):
		return True

	def getCodeInfoList(self):
		return self.codeInfoList

	def getStructureList(self):
		return []

	def setCompositions(self):
		pass

class HanZiWrapperStructure(HanZiStructure):
	def __init__(self, referenceNode, expression):
		super().__init__()

		self.referenceNode=referenceNode
		self.expression=expression
		self.codeInfoList=[]

	def __str__(self):
		return self.getReferenceExpression()

	def isWrapper(self):
		return True

	def getReferenceExpression(self):
		return self.expression

	def getCodeInfoList(self):
		codeInfoList=[]
		for structure in self.getStructureList():
			codeInfoList.extend(structure.getCodeInfoList())
		return codeInfoList

	def getStructureList(self):
		tempList=self.expression.split(".")
		if(len(tempList)>1):
			referenceName=tempList[0]
			index=int(tempList[1])
			structureList=self.referenceNode.getSubStructureList(index)
		else:
			structureList=self.referenceNode.getStructureList()
		return structureList

class HanZiAssemblageStructure(HanZiStructure):
	def __init__(self, operator, structureList):
		super().__init__()

		self.operator=operator
		self.structureList=structureList

		self.codeInfoList=[]

	def __str__(self):
		structureList=self.getStructureList()
		nameList=[structure.getUniqueName() for structure in structureList]
		return "(%s %s)"%(self.getOperator().getName(), " ".join(nameList))

	def isAssemblage(self):
		return True

	def getOperator(self):
		return self.operator

	def getCodeInfoList(self):
		return self.codeInfoList

	def getStructureList(self):
		return self.structureList

	def setCompositions(self):
		structureList=self.getStructureList()
		infoListList=HanZiAssemblageStructure.getAllCodeInfoListFromNodeList(structureList)

		codeInfoManager=StateManager.getCodeInfoManager()
		for infoList in infoListList:
			codeInfo=codeInfoManager.encodeToCodeInfo(self.operator, infoList)
			if codeInfo!=None:
				for childCodeInfo in infoList:
					codeVariance=childCodeInfo.getCodeVarianceType()
					codeInfo.multiplyCodeVarianceType(codeVariance)

				self.codeInfoList.append(codeInfo)

	@staticmethod
	def getAllCodeInfoListFromNodeList(structureList):
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

		for structure in structureList:
			tmpCodeInfoList=structure.getCodeInfoList()
			codeInfoList=filter(lambda x: x.isSupportRadixCode(), tmpCodeInfoList)
			infoListList=combineList(infoListList, codeInfoList)

		return infoListList


class HanZiNode:
	def __init__(self, name):
		self.name=name
		self.structureList=[]

		characterInfo=CharacterInfo.CharacterInfo(self.name)
		self.characterInfo=characterInfo

	def getName(self):
		return self.name

	def addStructure(self, structure):
		self.structureList.append(structure)

	def setStructureList(self, structureList):
		self.structureList=structureList

	def getStructureList(self):
		return self.structureList

	def getStructureListWithCondition(self):
		return self.structureList

	def getSubStructureList(self, index):
		subStructureList=[]
		for structure in self.structureList:
			structureList=structure.getStructureList()
			subStructureList.append(structureList[index])
		return subStructureList

	def getCodeInfoList(self):
		structureList=self.getStructureListWithCondition()

		return sum(map(lambda s: s.getCodeInfoList(), structureList), [])

	def getCharacterInfo(self):
		codeInfoList=self.getCodeInfoList()
		self.characterInfo.setCodeInfoList(codeInfoList)

		return self.characterInfo

	def printAllCodeInfoInStructure(self):
		structureList=self.getStructureListWithCondition()
		for struct in structureList:
			struct.printAllCodeInfo()


class HanZiNetwork:
	def __init__(self):
		self.nodeDict={}
		self.structureDict={}

		self.nodeExpressionDict={}

	def addNode(self, name):
		if name not in self.nodeDict:
			tmpNode=HanZiNode(name)
			self.nodeDict[name]=tmpNode

	def addStructure(self, structureName, structure):
		self.structureDict[structureName]=structure

	def addStructureIntoNode(self, structure, nodeName):
		dstNode=self.findNode(nodeName)
		dstNode.addStructure(structure)

	def findNode(self, nodeName):
		return self.nodeDict.get(nodeName)

	def getCharacterInfo(self, charName):
		charNode=self.nodeDict.get(charName)
		characterInfo=None
		if charNode:
			characterInfo=charNode.getCharacterInfo()
		return characterInfo

	def generateOperator(self, operatorName):
		operator=StateManager.getOperationManager().generateOperator(operatorName)
		return operator

	def generateAssemblageStructure(self, operator, structureList):
		structure=HanZiStructure.generateAssemblage(operator, structureList)
		return structure

	def generateWrapperStructure(self, name, nodeExpression):
		if nodeExpression in self.nodeExpressionDict:
			return self.nodeExpressionDict[nodeExpression]
		rootNode=self.findNode(name)
		structure=HanZiStructure.generateWrapper(rootNode, nodeExpression)
		self.nodeExpressionDict[nodeExpression]=structure
		return structure

	def generateUnitStructure(self, radixCodeInfo):
		structure=HanZiStructure.generateUnit(radixCodeInfo)
		return structure

