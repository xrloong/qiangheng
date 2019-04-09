from injector import inject

from .network import HanZiNetwork
from .helper import HanZiProcessor
from .helper import StructureFactory

from model.manager import OperatorManager
from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import RadixManager
from model.util import TreeRegExp

class TreeProxyOfStageAddStructure(TreeRegExp.BasicTreeProxy):
	def __init__(self, structureFactory, operationManager):
		self.operationManager = operationManager
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
		return self.structureFactory.generateWrapperStructure(nodeName)

	def generateLeafNodeByReference(self, referencedNode, index):
		nodeName=referencedNode.getTag().getReferenceName()
		return self.structureFactory.generateWrapperStructure(nodeName, index)

	def generateNode(self, operatorName, children):
		operator=self.operationManager.generateOperator(operatorName)
		return self.structureFactory.generateAssemblageStructure(operator, children)


class TaskAddNode:
	# 加入如 "相" "[漢右]" 的節點。
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork,
			radixManager: RadixManager,
			structureFactory: StructureFactory):
		self.hanziNetwork = hanziNetwork
		self.radixManager = radixManager
		self.structureFactory = structureFactory

	def handleCharacter(self, character):
		from model.element import CharacterInfo

		characterInfo=CharacterInfo.CharacterInfo(character)
		self.hanziNetwork.addNode(character, characterInfo)

		if self.radixManager.hasRadix(character):
			radixInfoList=self.radixManager.getRadixCodeInfoList(character)
			for radixCodeInfo in radixInfoList:
				structure = self.structureFactory.generateUnitStructure(radixCodeInfo)
				self.hanziNetwork.addUnitStructureIntoNode(structure, character)


class TaskAddStructure:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork, structureManager: StructureManager,
			operationManager: OperatorManager,
			structureFactory: StructureFactory):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager
		self.structureFactory = structureFactory
		self.treeProxy=TreeProxyOfStageAddStructure(structureFactory, operationManager)

	def handleCharacter(self, character):
		self.expandNode(character)

	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def expandNode(self, nodeName):
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
			self.expandNode(referenceNode.getName())

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
			self.expandNode(referenceNode.getName())

		tag=structure.getTag()
		if tag.isSubstituteApplied():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureBySubstitute(childStructure, substituteRuleList)

		tag.setSubstituteApplied()

	def rearrangeStructure(self, structure, substituteRuleList):
		def expandLeaf(structure):
			nodeName=structure.getReferenceName()

			if nodeName:
				self.expandNode(nodeName)

			children=structure.getStructureList()
			for child in children:
				expandLeaf(child)

		def rearrangeStructureOneTurn(structure, filteredSubstituteRuleList):
#			expandLeaf(structure)

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

		l=nodeExpression.split(".")
		if len(l)>1:
			subIndex=int(l[1])
		else:
			subIndex=0

		return self.structureFactory.generateWrapperStructure(name, subIndex)

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList=self.structureManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator=structDesc.getOperator()

		return self.structureFactory.generateAssemblageStructure(operator, childStructureList)

class ComputeCharacterInfo:
	@inject
	def __init__(self, structureManager: StructureManager,
			taskAddNode: TaskAddNode,
			taskAddStructure: TaskAddStructure,

			hanziNetwork: HanZiNetwork,
			hanziProcessor: HanZiProcessor
			):
		self.structureManager = structureManager

		self.taskAddNode = taskAddNode
		self.taskAddStructure = taskAddStructure

		self.hanziNetwork = hanziNetwork
		self.hanziProcessor = hanziProcessor

	def compute(self, characterSet = None):
		characters = self.structureManager.getAllCharacters()
		for character in characters:
			self.taskAddNode.handleCharacter(character)

		characterSet = characterSet if characterSet != None else characters
		for character in characterSet:
			self.taskAddStructure.handleCharacter(character)

			node = self.hanziNetwork.findNode(character)
			self.hanziProcessor.computeCodeInfosOfNodeTree(node)

