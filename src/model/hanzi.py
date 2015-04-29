class HanZiStructure:
	def __init__(self, tag):
		self.referenceNode=None
		self.operator=None
		self.structureList=[]

		self.tag=tag

	def __str__(self):
		tag=self.getTag()
		if tag.isAssemblage():
			structureList=self.getStructureList()
			nameList=[str(structure) for structure in structureList]
			return "(%s %s)"%(self.getOperator(), " ".join(nameList))
		return str(self.tag)

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

	def getStructureList(self):
		if self.referenceNode:
			return self.getWrapperStructureList()
		return self.structureList

	def getWrapperStructureList(self):
		expression=self.getTag().getReferenceExpression()
		tempList=expression.split(".")
		if(len(tempList)>1):
			referenceName=tempList[0]
			index=int(tempList[1])-1
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

	def __str__(self):
		return self.name

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

	def addNode(self, name, tag):
		if name not in self.nodeDict:
			node=HanZiNode(name, tag)
			self.nodeDict[name]=node

	def findNode(self, nodeName):
		return self.nodeDict.get(nodeName)

	def isNodeExpanded(self, nodeName):
		node=self.nodeDict.get(nodeName)
		structureList=node.getStructureList()
		return len(structureList)>0

	def addStructure(self, structureName, structure):
		self.structureDict[structureName]=structure

	def addStructureIntoNode(self, structure, nodeName):
		dstNode=self.findNode(nodeName)
		dstNode.addStructure(structure)

	def generateStructure(self, tag, referenceNode=None, compound=[]):
		structure=HanZiStructure(tag)

		if referenceNode:
			structure.setAsWrapper(referenceNode)

		if compound:
			operator, structureList = compound
			structure.setAsCompound(operator, structureList)

		return structure

