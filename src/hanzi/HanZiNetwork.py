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

		self.addNodeIntoNetwork(structDesc)

	def addNodeIntoNetwork(self, structDesc):
		self.hanziNetwork.addNode(structDesc)

	def queryDescription(self, characterName):
		return self.descriptionManager.queryCharacterDescription(characterName)



class HanZiNetwork:
	def __init__(self):
		self.nodeList=[]

		self.structDescUniqueNameToNodeDict={}
		self.structDescExpandNameToNodeDict={}

	@staticmethod
	def construct(descriptionManager):
		toHanZiNetworkConverter=DescriptionManagerToHanZiNetworkConverter(descriptionManager)
		return toHanZiNetworkConverter.constructDescriptionNetwork()

	def addNamedNode(self, name, characterProperty):
		tmpNode=HanZiNode.HanZiNode(name, characterProperty)
		self.structDescUniqueNameToNodeDict[name]=tmpNode
		self.structDescExpandNameToNodeDict[name]=tmpNode

	def addAnonymousNode(self, structDesc):
		anonymousName=structDesc.getUniqueName()
		if anonymousName not in self.structDescUniqueNameToNodeDict:
			tmpNode=HanZiNode.HanZiNode(anonymousName)
			self.structDescUniqueNameToNodeDict[anonymousName]=tmpNode

	def addNode(self, structDesc):
		self.addAnonymousNode(structDesc)
		if structDesc.isLeaf():
			self.addReferenceLink(structDesc)
		elif structDesc.isTurtle():
			self.addUnitLink(structDesc)
		else:
			self.addLink(structDesc)

	def addReferenceLink(self, structDesc):
		expression=structDesc.getReferenceExpression()
		rootNode=self.structDescExpandNameToNodeDict.get(structDesc.getReferenceName())

		structure=HanZiStructure.HanZiWrapperStructure(rootNode, expression)

		dstNode=self.findNode(structDesc)
		dstNode.addStructure(structure)

	def addUnitLink(self, structDesc):
		codeType=structDesc.getCodeType()
		codeInfoProperties=structDesc.getCodeInfoDict()
		structure=HanZiStructure.HanZiUnitStructure(codeType, codeInfoProperties)

		dstNode=self.findNode(structDesc)
		dstNode.addStructure(structure)

	def addLink(self, structDesc):
		operator=structDesc.getOperator()
		childDescList=structDesc.getCompList()
		if len(childDescList)>0:
			childNodeList=[self.findNode(childDesc) for childDesc in childDescList]

			codeType=structDesc.getCodeType()
			structure=HanZiStructure.HanZiAssemblageStructure(codeType, operator, childNodeList)

			dstNode=self.findNode(structDesc)
			dstNode.addStructure(structure)

	def findNode(self, structDesc):
		if structDesc.isRoot():
			return self.structDescExpandNameToNodeDict.get(structDesc.getRootName())
		elif structDesc.isLeaf():
			return self.structDescUniqueNameToNodeDict.get(structDesc.getUniqueName())
		else:
			return self.structDescUniqueNameToNodeDict.get(structDesc.getUniqueName())

	def getCodePropertiesList(self, charName):
		charNode=self.structDescExpandNameToNodeDict.get(charName)
		charProp=charNode.getCharacterProperty()
		freq=charProp.getFrequency()

		codePropList=charNode.getCodePropertiesList()
		return map(lambda codeAndType: codeAndType+[freq], codePropList)

