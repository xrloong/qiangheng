import copy
from description.CodeType import CodeType
from description.operator import Operator

from . import HanZiNode

class DescriptionManagerToHanZiNetworkConverter:
	def __init__(self, descriptionManager):
		self.descriptionManager=descriptionManager
		self.hanziNetwork=HanZiNetwork()

	def constructDescriptionNetwork(self):
		charNameList=self.descriptionManager.getAllCharacters()
		sortedNameList=sorted(charNameList)

		for charName in sortedNameList:
			self.hanziNetwork.addNamedNode(charName)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)

			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				structDesc.setRootName(charName)
				self.recursivelyAddStructure(structDesc)
		return self.hanziNetwork

	def recursivelyAddStructure(self, structDesc):
		hanziNetwork=self.hanziNetwork

		if structDesc.isLeaf():
			hanziNetwork.addReferenceNode(structDesc)
		elif structDesc.isTurtle():
			hanziNetwork.addTurtleStruct(structDesc)
		else:
			hanziNetwork.addNode(structDesc)
			operator=structDesc.getOperator()
			childDescList=structDesc.getCompList()

			for childSrcDesc in childDescList:
				self.recursivelyAddStructure(childSrcDesc)

			hanziNetwork.addLink(structDesc, operator, childDescList)

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

	def addNamedNode(self, name):
		tmpNode=HanZiNode.HanZiNode(name)
		self.structDescUniqueNameToNodeDict[name]=tmpNode
		self.structDescExpandNameToNodeDict[name]=tmpNode

	def addNode(self, structDesc):
		anonymousName=structDesc.getUniqueName()
		if anonymousName not in self.structDescUniqueNameToNodeDict:
			tmpNode=HanZiNode.HanZiNode(anonymousName)
			self.structDescUniqueNameToNodeDict[anonymousName]=tmpNode

	def addReferenceNode(self, structDesc):
		anonymousName=structDesc.getUniqueName()
		if anonymousName not in self.structDescUniqueNameToNodeDict:
			expression=structDesc.getReferenceExpression()
			rootNode=self.structDescExpandNameToNodeDict.get(structDesc.getReferenceName())
			tmpNode=HanZiNode.HanZiWrapperNode(rootNode, expression)
			self.structDescUniqueNameToNodeDict[anonymousName]=tmpNode

	def addTurtleStruct(self, structDesc):
		self.addNode(structDesc)

		dstNode=self.findNode(structDesc)

		codeType=structDesc.getCodeType()

		codeInfoProperties=structDesc.getCodeInfoDict()

		codeType=structDesc.getCodeType()
		structure=HanZiNode.HanZiStructure(codeType, None, [])

		codeInfo=HanZiNode.HanZiCodeInfo(codeInfoProperties, codeType)
		structure.appendCodeInfo(codeInfo)

		structure.setToComponent()

		dstNode.addStructure(structure)

	def addLink(self, structDesc, operator, childDescList):
		if len(childDescList)>0:
			childNodeList=[self.findNode(childDesc) for childDesc in childDescList]
			dstNode=self.findNode(structDesc)

			codeType=structDesc.getCodeType()
			structure=HanZiNode.HanZiStructure(codeType, operator, childNodeList)
			structure.setToRadix()

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
		return charNode.getCodePropertiesList()

