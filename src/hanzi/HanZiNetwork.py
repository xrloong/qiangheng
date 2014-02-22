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

		# 將 referenceNode 轉為 targetNode
		# 如焤會使用 "府.0" 及 "府.1" ，則 "府" 為 referenceNode
		# 而 "广" 及 "付" 為 targetNode 。
		# 因有可能先建構 "焤" 的結構後，才建構 "府"
		# 所以在建構 "焤" 時， "府.0" 及 "府.1" 還不存在
		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)

			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				node=self.hanziNetwork.findNode(structDesc)
				strctureList=node.getStructureListWithCondition()
				for structure in strctureList:
					self.recursivelyConvertReferenceNodeToTargetNode(structure)
		return self.hanziNetwork

	def computeTargetNodeOfWrapperStrcture(self, wrapperStructuer):
		expression=wrapperStructuer.getExpression()
		tempList=expression.split(".")
		if(len(tempList)>1):
			referenceName=tempList[0]
			index=int(tempList[1])
			referenceNode=self.hanziNetwork.structDescUniqueNameToNodeDict.get(referenceName)
			targetNode=self.hanziNetwork.structDescUniqueNameToNodeDict.get(expression)
			targetNode.setStructureList(referenceNode.getSubStructureList(index))
			return targetNode

		else:
			return wrapperStructuer.referenceNode

	def recursivelyConvertReferenceNodeToTargetNode(self, structure):
		if isinstance(structure, HanZiStructure.HanZiWrapperStructure):
			targetNode=self.computeTargetNodeOfWrapperStrcture(structure)
			structure.setTargetNode(targetNode)
		else:
			nodeList=structure.getNodeList()
			for node in nodeList:
				strctureList=node.getStructureListWithCondition()
				for childStructure in strctureList:
					self.recursivelyConvertReferenceNodeToTargetNode(childStructure);

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
		hanziNetwork=toHanZiNetworkConverter.constructDescriptionNetwork()
		hanziNetwork.setCompositionsOfAllNodes()
		return hanziNetwork

	def setCompositionsOfAllNodes(self):
		for node in self.structDescExpandNameToNodeDict.values():
			node.setNodeTree()

	def addNamedNode(self, name, characterProperty):
		if name not in self.structDescUniqueNameToNodeDict:
			tmpNode=HanZiNode.HanZiNode(name, characterProperty)
			self.structDescUniqueNameToNodeDict[name]=tmpNode
			self.structDescExpandNameToNodeDict[name]=tmpNode

	def addAnonymousNode(self, structDesc):
		anonymousName=structDesc.getUniqueName()
		if anonymousName not in self.structDescUniqueNameToNodeDict:
			tmpNode=HanZiNode.HanZiNode(anonymousName)
			self.structDescUniqueNameToNodeDict[anonymousName]=tmpNode

	def addNode(self, structDesc):
		if structDesc.isLeaf():
			expression=structDesc.getReferenceExpression()
			self.addNamedNode(expression, None)
			self.addAnonymousNode(structDesc)
			self.addReferenceLink(structDesc)
		elif structDesc.isTurtle():
			self.addAnonymousNode(structDesc)
			self.addUnitLink(structDesc)
		else:
			self.addAnonymousNode(structDesc)
			self.addLink(structDesc)

	def addReferenceLink(self, structDesc):
		expression=structDesc.getReferenceExpression()
		name=structDesc.getReferenceName()
#		rootNode=self.structDescExpandNameToNodeDict.get(name)
		rootNode=self.structDescExpandNameToNodeDict.get(expression)

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

