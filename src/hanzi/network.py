from injector import inject

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


class HanZiNetwork:
	@inject
	def __init__(self):
		self.nodeDict={}
		self.structureDict={}

	def addNode(self, name, tag):
		if name not in self.nodeDict:
			node=HanZiNode(name, tag)
			self.nodeDict[name]=node

	def findNode(self, nodeName):
		return self.nodeDict.get(nodeName)

	def isNodeExpanded(self, nodeName):
		node=self.nodeDict.get(nodeName)
		structure=node.getStructure()
		return bool(structure)

	def addStructure(self, structureName, structure):
		self.structureDict[structureName]=structure

	def addStructureIntoNode(self, structure, nodeName):
		dstNode=self.findNode(nodeName)
		dstNode.setStructure(structure)

	def addUnitStructureIntoNode(self, structure, nodeName):
		dstNode=self.findNode(nodeName)
		dstNode.addUnitStructure(structure)

class HanZiNetworkNodeFinder:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork):
		self.hanziNetwork = hanziNetwork

	def findNode(self, nodeName):
		return self.hanziNetwork.findNode(nodeName)

