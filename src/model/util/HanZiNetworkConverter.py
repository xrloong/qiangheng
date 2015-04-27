from . import TreeRegExp
from ..hanzi import HanZiNetwork
from model import StateManager

class StructureTag:
	def __init__(self):
		self.codeInfoList=[]

		self.flagIsCodeInfoGenerated=False
		self.flagIsTemplateApplied=False
		self.flagIsSubstituteApplied=False

	def isUnit(self):
		return False

	def isWrapper(self):
		return False

	def isAssemblage(self):
		return False

	def isCodeInfoGenerated(self):
		return self.flagIsCodeInfoGenerated

	def isTemplateApplied(self):
		return self.flagIsTemplateApplied

	def isSubstituteApplied(self):
		return self.flagIsSubstituteApplied

	def setCodeInfoGenerated(self):
		self.flagIsCodeInfoGenerated=True

	def setTemplateApplied(self):
		self.flagIsTemplateApplied=True

	def setSubstituteApplied(self):
		self.flagIsSubstituteApplied=True

	def setCodeInfoList(self, codeInfoList):
		self.codeInfoList=codeInfoList

	def getCodeInfoList(self):
		return self.codeInfoList

	def printAllCodeInfo(self):
		for codeInfo in self.getCodeInfoList():
			pass

	def getReferenceExpression(self):
		return None

	def generateCodeInfos(self, operator, tagList):
		pass

class StructureUnitTag(StructureTag):
	def __init__(self, radixCodeInfo):
		super().__init__()
		self.codeInfoList=[radixCodeInfo]

	def __str__(self):
		return str(self.codeInfoList)

	def isUnit(self):
		return True

	def getCodeInfoList(self):
		return self.codeInfoList

class StructureWrapperTag(StructureTag):
	def __init__(self, referenceExpression):
		super().__init__()
		self.referenceExpression=referenceExpression

	def __str__(self):
		return self.getReferenceExpression()

	def isWrapper(self):
		return True

	def getReferenceExpression(self):
		return self.referenceExpression

	def generateCodeInfos(self, operator, tagList):
		codeInfoList=[]
		for tag in tagList:
			codeInfoList.extend(tag.getCodeInfoList())
		self.setCodeInfoList(codeInfoList)

class StructureAssemblageTag(StructureTag):
	def __init__(self):
		super().__init__()

	def isAssemblage(self):
		return True

	def setInfoListList(self, operator, infoListList):
		codeInfoManager=StateManager.getCodeInfoManager()
		codeInfoList=[]
		for infoList in infoListList:
			codeInfo=codeInfoManager.encodeToCodeInfo(operator, infoList)
			if codeInfo!=None:
				for childCodeInfo in infoList:
					codeVariance=childCodeInfo.getCodeVarianceType()
					codeInfo.multiplyCodeVarianceType(codeVariance)

				codeInfoList.append(codeInfo)
		self.setCodeInfoList(codeInfoList)

	def generateCodeInfos(self, operator, tagList):
		infoListList=StructureAssemblageTag.getAllCodeInfoListFragTagList(tagList)
		self.setInfoListList(operator, infoListList)

	@staticmethod
	def getAllCodeInfoListFragTagList(tagList):
		def combineList(infoListList, infoListOfNode):
			if len(infoListList)==0:
				ansListList=[]
				for codeInfo in infoListOfNode:
					ansListList.append([codeInfo])
			else:
				ansListList=[]
				for infoList in infoListList:
					for codeInfo in infoListOfNode:
						ansListList.append(infoList+[codeInfo])

			return ansListList

		infoListList=[]

		for tag in tagList:
			tmpCodeInfoList=tag.getCodeInfoList()
			codeInfoList=filter(lambda x: x.isSupportRadixCode(), tmpCodeInfoList)
			infoListList=combineList(infoListList, codeInfoList)

		return infoListList



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
		def __init__(self, hanziNetwork, stage):
			self.hanziNetwork = hanziNetwork
			self.stage = stage

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
				elif tree.isWrapper():
					referenceNode=tree.getReferenceNode()
					structureList=referenceNode.getStructureList()
					if structureList:
						structure=referenceNode.getStructureList()[0]
						isMatch &= prop.get("運算") == structure.getOperator().getName()
					else:
						isMatch = False
				else:
					isMatch = False

			return isMatch

		def generateLeafNode(self, nodeExpression):
			name=nodeExpression.split(".")[0]
			structure = self.stage.generateWrapperStructure(name, nodeExpression)
			return structure

		def generateLeafNodeByReference(self, referencedNode, index):
			nodeExpression="%s.%d"%(referencedNode.getTag().getReferenceExpression(), index)
			return self.generateLeafNode(nodeExpression)

		def generateNode(self, operatorName, children):
			operator=self.stage.generateOperator(operatorName)
			structure = self.stage.generateAssemblageStructure(operator, children)
			return structure

	def __init__(self, hanziNetwork, structureManager):
		super().__init__(hanziNetwork, structureManager)
		self.treeProxy=StageAddStructure.TreeProxy(self.hanziNetwork, self)
		self.nodeExpressionDict={}

	def execute(self):
		for charName in self.getCharNameList():
			self.expandNode(charName)

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

			templateRuleList=self.structureManager.getTemplateRuleList()
			self.recursivelyRearrangeStructureByTemplate(structure, templateRuleList)
			substituteRuleList=self.structureManager.getSubstituteRuleList()
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

		structure=self.generateWrapperStructure(name, nodeExpression)
		return structure

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList=self.structureManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator=structDesc.getOperator()
		structure=self.generateAssemblageStructure(operator, childStructureList)
		return structure

	def generateOperator(self, operatorName):
		operator=StateManager.getOperationManager().generateOperator(operatorName)
		return operator

	def generateAssemblageStructure(self, operator, structureList):
		tag=StructureAssemblageTag()
		structure=self.hanziNetwork.generateStructure(tag, compound=[operator, structureList])
		return structure

	def generateWrapperStructure(self, name, nodeExpression):
		if nodeExpression in self.nodeExpressionDict:
			return self.nodeExpressionDict[nodeExpression]

		rootNode=self.hanziNetwork.findNode(name)

		tag=StructureWrapperTag(nodeExpression)
		structure=self.hanziNetwork.generateStructure(tag, referenceNode=rootNode)

		self.nodeExpressionDict[nodeExpression]=structure
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
		tag=StructureUnitTag(radixCodeInfo)
		structure=self.hanziNetwork.generateStructure(tag)
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

