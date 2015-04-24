from . import TreeRegExp
from ..hanzi import HanZiNetwork

class ConversionStage:
	def __init__(self, hanziNetwork, structureManager):
		self.hanziNetwork=hanziNetwork
		self.structureManager=structureManager

	def getCharNameList(self):
		return self.structureManager.getAllCharacters()

	def execute(self):
		pass

class StageAddNode(ConversionStage):
	def __init__(self, hanziNetwork, structureManager):
		super().__init__(hanziNetwork, structureManager)

	def execute(self):
		# 加入如 "相" "[漢右]" 的節點。
		for charName in self.getCharNameList():
			self.hanziNetwork.addNode(charName)

class StageAddStructure(ConversionStage):
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

	def __init__(self, hanziNetwork, structureManager):
		super().__init__(hanziNetwork, structureManager)
		self.treeProxy=StageAddStructure.TreeProxy(self.hanziNetwork)

	def execute(self):
		for charName in self.getCharNameList():
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

	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

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

	def generateReferenceLink(self, structDesc):
		name=structDesc.getReferenceName()
		nodeExpression=structDesc.getReferenceExpression()

		structure=self.hanziNetwork.generateWrapperStructure(name, nodeExpression)
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

class StageAddCodeInfo(ConversionStage):
	def __init__(self, hanziNetwork, structureManager):
		super().__init__(hanziNetwork, structureManager)

	def execute(self):
		codeInfoManager=self.structureManager.getCodeInfoManager()
		for charName in self.getCharNameList():
			if codeInfoManager.hasRadix(charName):
				radixInfoList=codeInfoManager.getRadixCodeInfoList(charName)
				for radixCodeInfo in radixInfoList:
					structure=self.generateUnitLink(radixCodeInfo)
					self.hanziNetwork.addStructureIntoNode(structure, charName)

	def generateUnitLink(self, radixCodeInfo):
		structure=self.hanziNetwork.generateUnitStructure(radixCodeInfo)
		return structure

class StageSetNodeTree(ConversionStage):
	def __init__(self, hanziNetwork, structureManager):
		super().__init__(hanziNetwork, structureManager)

	def execute(self):
		for charName in self.getCharNameList():
			node=self.hanziNetwork.findNode(charName)
			self.setNodeTree(node)

	def setNodeTree(self, node):
		"""設定某一個字符所包含的部件的碼"""

		structureList=node.getStructureListWithCondition()

		for structure in structureList:
			self.setStructureTree(structure)

	def setStructureTree(self, structure):
		if structure.flagIsSet:
			return

		structure.flagIsSet=True

		structureList=structure.getStructureList()
		for s in structureList:
			self.setStructureTree(s)

		structure.setCompositions()

class StageGetCharacterInfo(ConversionStage):
	def __init__(self, hanziNetwork, structureManager):
		super().__init__(hanziNetwork, structureManager)
		self.characterInfoList=[]

	def execute(self):
		characterInfoList=[]
		for charName in sorted(self.getCharNameList()):
			characterInfo=None

			charNode=self.hanziNetwork.findNode(charName)
			if charNode:
				characterInfo=charNode.getCharacterInfo()

			if characterInfo:
				characterInfoList.append(characterInfo)
		self.characterInfoList=characterInfoList

	def getCharacterInfoList(self):
		return self.characterInfoList

class ComputeCharacterInfo:
	def __init__(self):
		pass

	def compute(self, structureManager):
		hanziNetwork=HanZiNetwork()

		StageAddNode(hanziNetwork, structureManager).execute()
		StageAddStructure(hanziNetwork, structureManager).execute()
		StageAddCodeInfo(hanziNetwork, structureManager).execute()
		StageSetNodeTree(hanziNetwork, structureManager).execute()

		stage=StageGetCharacterInfo(hanziNetwork, structureManager)
		stage.execute()

		return stage.getCharacterInfoList()

