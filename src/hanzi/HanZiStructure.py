import sys
from state import StateManager

class HanZiStructure:
	def __init__(self):
		self.flagIsSet=False

	def __str__(self):
		return self.getUniqueName()

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

	def setStructureTree(self):
		if self.flagIsSet:
			return

		self.flagIsSet=True

		structureList=self.getStructureList()
		for structure in structureList:
			structure.setStructureTree()

		self.setCompositions()

	def printAllCodeInfo(self):
		for codeInfo in self.getCodeInfoList():
			pass

class HanZiProxyStructure(HanZiStructure):
	def __init__(self, targetStructure):
		super().__init__()
		self.targetStructure=targetStructure
		self.historyStructures=[]

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

	def setCompositions(self):
		self.referenceNode.setNodeTree()

class HanZiAssemblageStructure(HanZiStructure):
	def __init__(self, operator, structureList):
		super().__init__()

		self.operator=operator
		self.structureList=structureList

		self.codeInfoList=[]

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


