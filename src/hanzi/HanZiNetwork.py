import sys
import copy

from util.topsort import topsort
from util.topsort import CycleError
from gear import Operator

from . import HanZiStructure
from . import HanZiNode

class DescriptionManagerToHanZiNetworkConverter:
	def __init__(self, descriptionManager):
		self.descriptionManager=descriptionManager
		self.hanziNetwork=HanZiNetwork()

	def constructDescriptionNetwork(self):
		sortedNameList=self.getSortedNameList()
#		print(sortedNameList, file=sys.stderr)

		# 加入如 "相" "[漢右]" 的節點。
		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)
			characterProperty=charDesc.getCharacterProperty()
			self.hanziNetwork.addNode(charName, characterProperty)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)

			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				structDesc.setRootName(charName)
				self.recursivelyAddStructure(structDesc)

		self.hanziNetwork.setNodeTreeByOrder(sortedNameList)
		return self.hanziNetwork

	def getSortedNameList(self, usingTopologicSorting=True):
		charNameList=self.descriptionManager.getAllCharacters()

		if usingTopologicSorting:
			try:
				pairList=[]
				startNodeName='[拓樸排序起始點]'
				endNodeName='[拓樸排序結束點]'
				for charName in charNameList:
					charDesc=self.queryDescription(charName)

					nameSet=set()
					structDescList=charDesc.getStructureList()
					for structDesc in structDescList:
						childNameSet=self.recursivelyFindAllReferenceNameSet(structDesc)
						nameSet=nameSet|childNameSet

					pairList.append([startNodeName, charName])
					pairList.append([charName, endNodeName])
					for referenceName in list(nameSet):
						pairList.append([referenceName, charName])

				sortedNameList=topsort(pairList)
				sortedNameList.remove(startNodeName)
				sortedNameList.remove(endNodeName)
			except CycleError as err:
				answer, num_parents, children = err.args
				print("有迴圈: {0}".format(children), file=sys.stderr)
				raise
		else:
			sortedNameList=sorted(charNameList)
		return sortedNameList

	def recursivelyFindAllReferenceNameSet(self, structDesc):
		if structDesc.isLeaf():
			name=structDesc.getReferenceName()
			nameSet={name}
		else:
			nameSet=set()
			childDescList=structDesc.getCompList()
			for childSrcDesc in childDescList:
				childNameSet=self.recursivelyFindAllReferenceNameSet(childSrcDesc)
				nameSet=nameSet|childNameSet
		return nameSet

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
		return hanziNetwork

	def setNodeTreeByOrder(self, nameList):
		for name in nameList:
			print("YYYYYYYY %s"%name, file=sys.stderr)
			node=self.nodeDict.get(name)
			node.setNodeTree()

	def addNode(self, name, characterProperty):
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
		codeVariance=structDesc.getCodeVarianceType()
		codeInfoProperties=structDesc.getCodeInfoDict()
		structure=HanZiStructure.HanZiUnitStructure(codeVariance, codeInfoProperties)

		return structure

	def addLink(self, structDesc):
		operator=structDesc.getOperator()
		childDescList=structDesc.getCompList()

		childStructureList=[self.findStructure(childDesc) for childDesc in childDescList]

		codeVariance=structDesc.getCodeVarianceType()
		structure=HanZiStructure.HanZiAssemblageStructure(codeVariance, operator, childStructureList)

		return structure

	def findNode(self, nodeName):
		return self.nodeDict.get(nodeName)

	def findStructure(self, structDesc):
		structureName=structDesc.getUniqueName()
		return self.structureDict.get(structureName)

	def getCharacterInfo(self, charName):
		charNode=self.nodeDict.get(charName)
		characterInfo=charNode.getCharacterInfo()
		return characterInfo

