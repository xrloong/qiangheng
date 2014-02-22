import sys
import copy
from description.CodeType import CodeType
from description.operator import Operator

from . import HanZiStructure
from . import HanZiNode

class DescriptionManagerToHanZiNetworkConverter:
	def __init__(self, descriptionManager):
		self.descriptionManager=descriptionManager
		self.hanziNetwork=HanZiNetwork()

	def constructDescriptionNetwork(self):
		charNameList=self.descriptionManager.getAllCharacters()
		sortedNameList=sorted(charNameList)

		# 加入如 "相" "[漢右]" 的節點。
		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)
			characterProperty=charDesc.getCharacterProperty()
			self.hanziNetwork.addNamedNode(charName, characterProperty)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)

			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				structDesc.setRootName(charName)
				self.recursivelyAddStructure(structDesc)

		return self.hanziNetwork

	def recursivelyAddStructure(self, structDesc):
		childDescList=structDesc.getCompList()
		for childSrcDesc in childDescList:
			self.recursivelyAddStructure(childSrcDesc)

		self.hanziNetwork.addStructure(structDesc)

	def queryDescription(self, characterName):
		return self.descriptionManager.queryCharacterDescription(characterName)



class HanZiNetwork:
	def __init__(self):
		self.nodeDict={}
		self.structureDict={}

	@staticmethod
	def construct(descriptionManager):
		toHanZiNetworkConverter=DescriptionManagerToHanZiNetworkConverter(descriptionManager)
		hanziNetwork=toHanZiNetworkConverter.constructDescriptionNetwork()
		hanziNetwork.setNodeTreeOfAllNodes()
		return hanziNetwork

	def setNodeTreeOfAllNodes(self):
		for node in self.nodeDict.values():
			node.setNodeTree()

	def addNamedNode(self, name, characterProperty):
		if name not in self.nodeDict:
			tmpNode=HanZiNode.HanZiNode(name, characterProperty)
			self.nodeDict[name]=tmpNode

	def addStructure(self, structDesc):
		if structDesc.isLeaf():
			structure=self.addReferenceLink(structDesc)
		elif structDesc.isTurtle():
			structure=self.addUnitLink(structDesc)
			self.addStructureIntoNode(structure, structDesc.getRootName())
		elif structDesc.isRoot():
			structure=self.addLink(structDesc)
			self.addStructureIntoNode(structure, structDesc.getRootName())
		else:
			structure=self.addLink(structDesc)

		structureName=structDesc.getUniqueName()
		self.structureDict[structureName]=structure

	def addStructureIntoNode(self, structure, nodeName):
		dstNode=self.findNode(nodeName)
		dstNode.addStructure(structure)

	def addReferenceLink(self, structDesc):
		expression=structDesc.getReferenceExpression()
		name=structDesc.getReferenceName()
		rootNode=self.nodeDict.get(name)

		structure=HanZiStructure.HanZiWrapperStructure(rootNode, expression)

		return structure

	def addUnitLink(self, structDesc):
		codeType=structDesc.getCodeType()
		codeInfoProperties=structDesc.getCodeInfoDict()
		structure=HanZiStructure.HanZiUnitStructure(codeType, codeInfoProperties)

		return structure

	def addLink(self, structDesc):
		operator=structDesc.getOperator()
		childDescList=structDesc.getCompList()

		childStructureList=[self.findStructure(childDesc) for childDesc in childDescList]

		codeType=structDesc.getCodeType()
		structure=HanZiStructure.HanZiAssemblageStructure(codeType, operator, childStructureList)

		return structure

	def findNode(self, nodeName):
		return self.nodeDict.get(nodeName)

	def findStructure(self, structDesc):
		structureName=structDesc.getUniqueName()
		return self.structureDict.get(structureName)

	def getCodePropertiesList(self, charName):
		charNode=self.nodeDict.get(charName)
		charProp=charNode.getCharacterProperty()
		freq=charProp.getFrequency()

		codePropList=charNode.getCodePropertiesList()
		return map(lambda codeAndType: codeAndType+[freq], codePropList)

