import sys

from util.topsort import topsort
from util.topsort import CycleError
from im.gear import Operator
from state import StateManager

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
			self.hanziNetwork.addNode(charName)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)
			structDescList=self.descriptionManager.queryStructureList(charDesc)
			for structDesc in structDescList:
				if structDesc.isEmpty():
					continue

				structure=self.recursivelyConvertDescriptionToStructure(structDesc)
				self.recursivelyAddStructure(structure)
				self.hanziNetwork.addStructureIntoNode(structure, charName)


		codeInfoManager=StateManager.getCodeInfoManager()
		for charName in sortedNameList:
			if codeInfoManager.hasRadix(charName):
				radixInfoList=codeInfoManager.getRadixCodeInfoList(charName)
				for radixCodeInfo in radixInfoList:
					structure=self.generateUnitLink(radixCodeInfo)
					self.hanziNetwork.addStructureIntoNode(structure, charName)

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

	def recursivelyConvertDescriptionToStructure(self, structDesc):
		if structDesc.isLeaf():
			structure=self.generateReferenceLink(structDesc)
		else:
			structure=self.generateLink(structDesc)

		structure.setUniqueName(structDesc.getUniqueName())
		return structure

	def recursivelyAddStructure(self, structure):
		for childStructure in structure.getStructureList():
			self.recursivelyAddStructure(childStructure)

		structureName=structure.getUniqueName()
		self.hanziNetwork.addStructure(structureName, structure)


	def queryDescription(self, characterName):
		return self.descriptionManager.queryCharacterDescription(characterName)

	def generateReferenceLink(self, structDesc):
		expression=structDesc.getReferenceExpression()
		name=structDesc.getReferenceName()
		rootNode=self.hanziNetwork.findNode(name)

		structure=HanZiStructure.HanZiWrapperStructure(rootNode, expression)

		return structure

	def generateUnitLink(self, radixCodeInfo):
		structure=HanZiStructure.HanZiUnitStructure(radixCodeInfo)
		return structure

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList=self.descriptionManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator=structDesc.getOperator()

		structure=HanZiStructure.HanZiAssemblageStructure(operator, childStructureList)
		return structure


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
#			print(name, file=sys.stderr)
			node=self.nodeDict.get(name)
			node.setNodeTree()

	def addNode(self, name):
		if name not in self.nodeDict:
			tmpNode=HanZiNode.HanZiNode(name)
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
		characterInfo=charNode.getCharacterInfo()
		return characterInfo

