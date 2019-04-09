from injector import inject
from .item import HanZiStructure
from .item import HanZiNode

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

	def generateStructure(self, tag, reference=[], compound=[]):
		structure=HanZiStructure(tag)

		if reference:
			referenceName, index = reference
			referenceNode=self.findNode(referenceName)
			structure.setAsWrapper(referenceNode, index)

		if compound:
			operator, structureList = compound
			structure.setAsCompound(operator, structureList)

		return structure

