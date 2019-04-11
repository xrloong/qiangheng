from injector import inject

from .network import HanZiNetwork
from .helper import HanZiProcessor
from .helper import StructureFactory

from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import RadixManager
from model.util import TreeRegExp

class TreeProxyOfStageAddStructure(TreeRegExp.BasicTreeProxy):
	def __init__(self, structureFactory):
		self.structureFactory = structureFactory

	def getChildren(self, tree):
		expanedStructure=tree.getExpandedStructure()
		return expanedStructure.getStructureList()

	def matchSingleQuickly(self, tre, tree):
		treOperatorName=tre.prop.get("運算")
		treeOperator=tree.getOperator()
		return treeOperator and (treOperatorName==None or treOperatorName==treeOperator.getName())

	def matchSingle(self, tre, tree):
		prop=tre.prop
		isMatch = True
		tag=tree.getTag()
		if "名稱" in prop:
			expressionName=prop.get("名稱")
			expanedStructure=tree.getExpandedStructure()
			isMatch = expressionName == tree.getReferenceExpression()

		if "運算" in prop:
			operatorName=prop.get("運算")
			expanedStructure=tree.getExpandedStructure()
			isMatch = operatorName == expanedStructure.getOperatorName()

		return isMatch

	def generateLeafNode(self, nodeName):
		return self.structureFactory.getWrapperStructureByNodeName(nodeName)

	def generateLeafNodeByReference(self, referencedNode, index):
		return self.structureFactory.getWrapperStructureByNode(referencedNode, index)

	def generateNode(self, operatorName, children):
		return self.structureFactory.getCompoundStructureByOperatorName(operatorName, children)


class TaskConstructNetwork:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork,
			structureManager: StructureManager,
			radixManager: RadixManager,
			structureFactory: StructureFactory
			):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager
		self.radixManager = radixManager
		self.structureFactory = structureFactory
		self.treeProxy=TreeProxyOfStageAddStructure(structureFactory)

	def construct(self, characters):
		for character in characters:
			self.handleAddNode(character)

		for character in characters:
			self.handleAddStructure(character)

	def handleAddNode(self, character):
		self.structureFactory.touchNode(character)

	def handleAddStructure(self, character):
		self.expandNodeByName(character)

	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def expandNodeByName(self, nodeName):
		node = self.hanziNetwork.findNode(nodeName)
		self.expandNode(node)

	def expandNode(self, node):
		character = node.getName()
		if self.radixManager.hasRadix(character) and len(node.getUnitStructureList())==0:
			radixInfoList=self.radixManager.getRadixCodeInfoList(character)
			for radixCodeInfo in radixInfoList:
				structure = self.structureFactory.getUnitStructure(radixCodeInfo)
				self.hanziNetwork.addUnitStructureIntoNode(structure, character)

		nodeName = character
		if self.hanziNetwork.isNodeExpanded(nodeName):
			return

		charDesc=self.queryDescription(nodeName)

		structDescList=charDesc.getStructureList()
		for structDesc in structDescList:
			if structDesc.isEmpty():
				continue

			structure=self.recursivelyConvertDescriptionToStructure(structDesc)

			templateRuleList=self.structureManager.getTemplateRules()
			self.recursivelyRearrangeStructureByTemplate(structure, templateRuleList)
			substituteRuleList=self.structureManager.getSubstituteRules()
			self.recursivelyRearrangeStructureBySubstitute(structure, substituteRuleList)

			self.recursivelyAddStructure(structure)
			self.hanziNetwork.addStructureIntoNode(structure, nodeName)

	def recursivelyConvertDescriptionToStructure(self, structDesc):
		if structDesc.isLeaf():
			structure=self.generateReferenceLink(structDesc)
		else:
			structure=self.generateLink(structDesc)

		return structure

	def recursivelyRearrangeStructureByTemplate(self, structure, substituteRuleList):
		referenceNode=structure.getReferenceNode()
		if referenceNode:
			self.expandNode(referenceNode)

		tag=structure.getTag()
		if tag.isTemplateApplied():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureByTemplate(childStructure, substituteRuleList)

		tag.setTemplateApplied()

	def recursivelyRearrangeStructureBySubstitute(self, structure, substituteRuleList):
		referenceNode=structure.getReferenceNode()
		if referenceNode:
			self.expandNode(referenceNode)

		tag=structure.getTag()
		if tag.isSubstituteApplied():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureBySubstitute(childStructure, substituteRuleList)

		tag.setSubstituteApplied()

	def rearrangeStructure(self, structure, substituteRuleList):
		def expandLeaf(structure):
			referenceNode=structure.getReferenceNode()
			if referenceNode:
				self.expandNode(referenceNode)

			children=structure.getStructureList()
			for child in children:
				expandLeaf(child)

		def rearrangeStructureOneTurn(structure, filteredSubstituteRuleList):
			changed=False
			for rule in filteredSubstituteRuleList:
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
			availableRuleFilter = lambda rule: TreeRegExp.matchQuickly(rule.getTRE(), structure, self.treeProxy)
			filteredSubstituteRuleList = filter(availableRuleFilter, substituteRuleList)
			changed=rearrangeStructureOneTurn(structure, filteredSubstituteRuleList)

	def recursivelyAddStructure(self, structure):
		for childStructure in structure.getStructureList():
			self.recursivelyAddStructure(childStructure)

		structureName=structure.getUniqueName()
		self.hanziNetwork.addStructure(structureName, structure)

	def generateReferenceLink(self, structDesc):
		name=structDesc.getReferenceName()
		nodeExpression=structDesc.getReferenceExpression()

		self.handleAddNode(name)

		l=nodeExpression.split(".")
		if len(l)>1:
			subIndex=int(l[1])
		else:
			subIndex=0

		return self.structureFactory.getWrapperStructureByNodeName(name, subIndex)

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList=self.structureManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator=structDesc.getOperator()

		return self.structureFactory.getCompoundStructure(operator, childStructureList)

class ComputeCharacterInfo:
	@inject
	def __init__(self,
			taskConstructNetwork: TaskConstructNetwork,

			structureManager: StructureManager,

			hanziNetwork: HanZiNetwork,
			hanziProcessor: HanZiProcessor
			):
		self.taskConstructNetwork = taskConstructNetwork

		self.structureManager = structureManager

		self.hanziNetwork = hanziNetwork
		self.hanziProcessor = hanziProcessor

	def compute(self, characterSet = None):
		characters = self.structureManager.getAllCharacters()
		characterSet = characterSet if characterSet != None else characters

		self.taskConstructNetwork.construct(characterSet)

		for character in characterSet:
			node = self.hanziNetwork.findNode(character)
			self.hanziProcessor.computeCodeInfosOfNodeTree(node)

