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
		from model.element import CharacterInfo
		# 加入如 "相" "[漢右]" 的節點。
		for charName in self.getCharNameList():
			characterInfo=CharacterInfo.CharacterInfo(charName)
			self.hanziNetwork.addNode(charName, characterInfo)

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
					isMatch &= prop.get("名稱") == tree.getTag().getReferenceExpression()
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
			nodeExpression="%s.%d"%(referencedNode.getTag().getReferenceExpression(), index)
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
		tag=structure.getTag()
		if tag.isTemplateApplied():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureByTemplate(childStructure, substituteRuleList)

		tag.setTemplateApplied()

	def recursivelyRearrangeStructureBySubstitute(self, structure, substituteRuleList):
		tag=structure.getTag()
		if tag.isSubstituteApplied():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureBySubstitute(childStructure, substituteRuleList)

		tag.setSubstituteApplied()

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

		structureList=node.getStructureList()

		for structure in structureList:
			self.recursivelyGenerateCodeInfoByStructureTree(structure)

	def recursivelyGenerateCodeInfoByStructureTree(self, structure):
		tag=structure.getTag()
		if tag.isCodeInfoGenerated():
			return

		for cihldStructure in structure.getStructureList():
			self.recursivelyGenerateCodeInfoByStructureTree(cihldStructure)
		structure.generateCodeInfos()

		tag.setCodeInfoGenerated()

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
				characterInfo=self.getNodeCharacterInfo(charNode)

			if characterInfo:
				characterInfoList.append(characterInfo)
		self.characterInfoList=characterInfoList

	def getCharacterInfoList(self):
		return self.characterInfoList

	def getNodeCharacterInfo(self, hanziNode):
		def getNodeCodeInfoList(hanziNode):
			structureList=hanziNode.getStructureList()

			return sum(map(lambda s: s.getTag().getCodeInfoList(), structureList), [])
		codeInfoList=getNodeCodeInfoList(hanziNode)
		characterInfo=hanziNode.getTag()
		characterInfo.setCodeInfoList(codeInfoList)

		return characterInfo

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

