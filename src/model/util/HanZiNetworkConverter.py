from . import TreeRegExp
from ..hanzi import HanZiNetwork

class HanZiNetworkConverter:
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
		self.treeProxy=HanZiNetworkConverter.TreeProxy(self.hanziNetwork)

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

				structure=self.recursivelyConvertDescriptionToStructure(structDesc)

				templateRuleList=self.structureManager.getTemplateRuleList()
				self.recursivelyRearrangeStructureByTemplate(structure, templateRuleList)
				substituteRuleList=self.structureManager.getSubstituteRuleList()
				self.recursivelyRearrangeStructureBySubstitute(structure, substituteRuleList)

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

	def recursivelyRearrangeStructureByTemplate(self, structure, substituteRuleList):
		if structure.isTemplateDone():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		structure.setTemplateDone()

		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureByTemplate(childStructure, substituteRuleList)

	def recursivelyRearrangeStructureBySubstitute(self, structure, substituteRuleList):
		if structure.isSubstituteDone():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		structure.setSubstituteDone()

		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureBySubstitute(childStructure, substituteRuleList)

	def rearrangeStructure(self, structure, substituteRuleList):
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
			operator=structure.getOperator()

			if operator:
				availableNameList = [None, operator.getName()]
				filteredSubstituteRuleList = [rule for rule in substituteRuleList if rule.getName() in availableNameList]
				changed=rearrangeStructureOneTurn(structure, filteredSubstituteRuleList)
			else:
				changed=False

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

