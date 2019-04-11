from injector import inject

from .network import HanZiNetwork
from .helper import HanZiCodeInfosComputer
from .helper import StructureFactory

from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import RadixManager
from model.tree.regexp import TreeRegExpInterpreter
from model.tree.regexp import BasicTreeProxy
from model.tree.regexp import TreeNodeGenerator

class HanZiTreeProxy(BasicTreeProxy):
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

class HanZiTreeNodeGenerator(TreeNodeGenerator):
	@inject
	def __init__(self, structureFactory: StructureFactory):
		self.structureFactory = structureFactory

	def generateLeafNode(self, nodeName):
		return self.structureFactory.getWrapperStructureByNodeName(nodeName)

	def generateLeafNodeByReference(self, referencedNode, index):
		return self.structureFactory.getWrapperStructureByNode(referencedNode, index)

	def generateNode(self, operatorName, children):
		return self.structureFactory.getCompoundStructureByOperatorName(operatorName, children)

class HanZiTreeRegExpInterpreter(TreeRegExpInterpreter):
	@inject
	def __init__(self, treeNodeGenerator: HanZiTreeNodeGenerator):
		super().__init__(HanZiTreeProxy(), treeNodeGenerator)

class ComputeCharacterInfo:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork,
			structureManager: StructureManager,
			radixManager: RadixManager,
			treInterpreter: HanZiTreeRegExpInterpreter,
			codeInfosComputer: HanZiCodeInfosComputer,
			structureFactory: StructureFactory
			):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager
		self.radixManager = radixManager
		self.codeInfosComputer = codeInfosComputer
		self.structureFactory = structureFactory

		self.treInterpreter = treInterpreter

	def compute(self, characters):
		for character in characters:
			self.constructCharacter(character)

	def constructCharacter(self, character):
		node = self.touchCharacter(character)
		self.expandNode(node)
		self.computeNode(node)

	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def touchCharacter(self, character):
		return self.structureFactory.touchNode(character)

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
		treInterpreter = self.treInterpreter
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

				tmpStructure = treInterpreter.matchAndReplace(tre, structure, result)
				if tmpStructure!=None:
					structure.setNewStructure(tmpStructure)
					structure=tmpStructure
					changed=True
					break
			return changed

		changed=True
		while changed:
			availableRuleFilter = lambda rule: treInterpreter.matchQuickly(rule.getTRE(), structure)
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

		self.constructCharacter(name)

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

	def computeNode(self, node):
		self.codeInfosComputer.computeForNode(node)

