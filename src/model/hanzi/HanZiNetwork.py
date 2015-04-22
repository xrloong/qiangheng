import sys

from ..element import Operator
from model.util import TreeRegExp

from . import HanZiStructure
from . import HanZiNode

class DescriptionManagerToHanZiNetworkConverter:
	class TreeProxy(TreeRegExp.BasicTreeProxy):
		def __init__(self, hanziNetwork):
			self.hanziNetwork = hanziNetwork

		def getChildren(self, tree):
			return tree.getStructureList()

		def matchSingle(self, tre, tree):
			prop=tre.prop
			isMatch = True
			if "名稱" in prop:
				if tree.isWrapper():
					isMatch &= prop.get("名稱") == tree.getReferenceExpression()
				else:
					isMatch = False

			if "運算" in prop:
				if tree.isAssemblage():
					isMatch &= prop.get("運算") == tree.getOperator().getName()
				else:
					isMatch = False

			return isMatch

		def generateLeafNode(self, nodeExpression):
			name=nodeExpression.split(".")[0]
			structure = self.hanziNetwork.generateWrapperStructure(name, nodeExpression)
			return structure

		def generateLeafNodeByReference(self, referencedNode, index):
			nodeExpression="%s.%d"%(referencedNode.getReferenceExpression(), index)
			return self.generateLeafNode(nodeExpression)

		def generateNode(self, operatorName, children):
			operator=self.hanziNetwork.generateOperator(operatorName)
			structure = self.hanziNetwork.generateAssemblageStructure(operator, children)
			return structure


	def __init__(self, structureManager):
		self.structureManager=structureManager
		self.hanziNetwork=HanZiNetwork()
		self.treeProxy=DescriptionManagerToHanZiNetworkConverter.TreeProxy(self.hanziNetwork)

	def constructDescriptionNetwork(self):
		charNameList=self.structureManager.getAllCharacters()

		# 加入如 "相" "[漢右]" 的節點。
		for charName in charNameList:
			charDesc=self.queryDescription(charName)
			self.hanziNetwork.addNode(charName)


		for charName in charNameList:
			charDesc=self.queryDescription(charName)

			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				if structDesc.isEmpty():
					continue

#				print("name: %s %s"%(charName, structDesc), file=sys.stderr);

				structure=self.recursivelyConvertDescriptionToStructure(structDesc)

				templateRuleList=self.structureManager.getTemplateRuleList()
				self.recursivelyRearrangeStructure(structure, templateRuleList)
				substituteRuleList=self.structureManager.getSubstituteRuleList()
				self.recursivelyRearrangeStructure(structure, substituteRuleList)

				self.recursivelyAddStructure(structure)
				self.hanziNetwork.addStructureIntoNode(structure, charName)

		codeInfoManager=self.structureManager.getCodeInfoManager()
		for charName in charNameList:
			if codeInfoManager.hasRadix(charName):
				radixInfoList=codeInfoManager.getRadixCodeInfoList(charName)
				for radixCodeInfo in radixInfoList:
					structure=self.generateUnitLink(radixCodeInfo)
					self.hanziNetwork.addStructureIntoNode(structure, charName)

		self.hanziNetwork.setNodeTreeByOrder(charNameList)
		return self.hanziNetwork

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

		return structure

	def recursivelyRearrangeStructure(self, structure, substituteRuleList):
		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructure(childStructure, substituteRuleList)

	def rearrangeStructure(self, structure, substituteRuleList):
		def rearrangeStructureOneTurn(structure, substituteRuleList):
			operator=structure.getOperator()

			if operator:
				filteredList = [rule for rule in substituteRuleList if rule.getName() in [None, operator.getName()]]
			else:
				return False

			changed=False
			for rule in filteredList:
				tre = rule.getTRE()
				result = rule.getReplacement()

				tmpStructure=TreeRegExp.matchAndReplace(tre, structure, result, self.treeProxy)
				if tmpStructure!=None:
					structure.setNewStructure(tmpStructure)
					structure=tmpStructure
					changed=True
					break
			return changed

		changed=True
		while changed:
			changed=rearrangeStructureOneTurn(structure, substituteRuleList)

	def recursivelyAddStructure(self, structure):
		for childStructure in structure.getStructureList():
			self.recursivelyAddStructure(childStructure)

		structureName=structure.getUniqueName()
		self.hanziNetwork.addStructure(structureName, structure)


	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def generateReferenceLink(self, structDesc):
		name=structDesc.getReferenceName()
		nodeExpression=structDesc.getReferenceExpression()

		structure=self.hanziNetwork.generateWrapperStructure(name, nodeExpression)
		return structure

	def generateUnitLink(self, radixCodeInfo):
		structure=self.hanziNetwork.generateUnitStructure(radixCodeInfo)
		return structure

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList=self.structureManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator=structDesc.getOperator()
		structure=self.hanziNetwork.generateAssemblageStructure(operator, childStructureList)
		return structure


class HanZiNetwork:
	def __init__(self):
		self.nodeDict={}
		self.structureDict={}

		self.nodeExpressionDict={}

	@staticmethod
	def construct(structureManager):
		toHanZiNetworkConverter=DescriptionManagerToHanZiNetworkConverter(structureManager)
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
		characterInfo=None
		if charNode:
			characterInfo=charNode.getCharacterInfo()
		return characterInfo

	def generateOperator(self, operatorName):
		from model import StateManager
		operator=StateManager.getOperationManager().generateOperator(operatorName)
		return operator

	def generateAssemblageStructure(self, operator, structureList):
		structure=HanZiStructure.generateAssemblage(operator, structureList)
		return structure

	def generateWrapperStructure(self, name, nodeExpression):
		if nodeExpression in self.nodeExpressionDict:
			return self.nodeExpressionDict[nodeExpression]
		rootNode=self.findNode(name)
		structure=HanZiStructure.generateWrapper(rootNode, nodeExpression)
		self.nodeExpressionDict[nodeExpression]=structure
		return structure

	def generateUnitStructure(self, radixCodeInfo):
		structure=HanZiStructure.generateUnit(radixCodeInfo)
		return structure

