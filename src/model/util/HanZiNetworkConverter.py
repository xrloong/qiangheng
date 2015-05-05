from . import TreeRegExp
from ..hanzi import HanZiNetwork
from model import StateManager

class StructureTag:
	def __init__(self):
		self.codeInfoList=[]

		self.flagIsCodeInfoGenerated=False
		self.flagIsTemplateApplied=False
		self.flagIsSubstituteApplied=False

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

	def generateCodeInfos(self, operator, tagList):
		pass

class StructureUnitTag(StructureTag):
	def __init__(self, radixCodeInfo):
		super().__init__()
		self.codeInfoList=[radixCodeInfo]

	def __str__(self):
		return str(self.codeInfoList)

	def getCodeInfoList(self):
		return self.codeInfoList

class StructureWrapperTag(StructureTag):
	def __init__(self, name, index):
		super().__init__()
		if index==0:
			referenceExpression="%s"%name
		else:
			referenceExpression="%s.%d"%(name, index)

		self.referenceName=name
		self.index=index
		self.referenceExpression=referenceExpression

	def __str__(self):
		return self.getReferenceExpression()

	def getIndex(self):
		return self.index

	def getReferenceName(self):
		return self.referenceName

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

		codeInfoManager=self.structureManager.getCodeInfoManager()
		# 加入如 "相" "[漢右]" 的節點。
		for charName in self.getCharNameList():
			characterInfo=CharacterInfo.CharacterInfo(charName)
			self.hanziNetwork.addNode(charName, characterInfo)

			if codeInfoManager.hasRadix(charName):
				radixInfoList=codeInfoManager.getRadixCodeInfoList(charName)
				for radixCodeInfo in radixInfoList:
					structure=self.generateUnitLink(radixCodeInfo)
					self.hanziNetwork.addUnitStructureIntoNode(structure, charName)

	def generateUnitLink(self, radixCodeInfo):
		tag=StructureUnitTag(radixCodeInfo)
		structure=self.hanziNetwork.generateStructure(tag)
		return structure


class StageAddStructure(ConversionStage):
	class TreeProxy(TreeRegExp.BasicTreeProxy):
		def __init__(self, hanziNetwork, stage):
			self.hanziNetwork = hanziNetwork
			self.stage = stage

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
			structure = self.stage.generateWrapperStructure(nodeName)
			return structure

		def generateLeafNodeByReference(self, referencedNode, index):
			nodeName=referencedNode.getTag().getReferenceName()
			structure = self.stage.generateWrapperStructure(nodeName, index)
			return structure

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

		structure=self.generateWrapperStructure(name, subIndex)
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

	def generateWrapperStructure(self, name, index=0):
		if (name, index) in self.nodeExpressionDict:
			return self.nodeExpressionDict[(name, index)]

		rootNode=self.hanziNetwork.findNode(name)

		tag=StructureWrapperTag(name, index)
		structure=self.hanziNetwork.generateStructure(tag, reference=[name, index])

		self.nodeExpressionDict[(name, index)]=structure
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

		structureList=node.getUnitStructureList()
		for structure in structureList:
			structure.generateCodeInfos()

		structure=node.getStructure()
		self.recursivelyGenerateCodeInfoByStructureTree(structure)

	def recursivelyGenerateCodeInfoByStructureTree(self, structure):
		if not structure:
			return

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
		structureList=hanziNode.getStructureList(True)
		codeInfoList=sum(map(lambda s: s.getTag().getCodeInfoList(), structureList), [])
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
		StageSetNodeTree(hanziNetwork, structureManager).execute()

		stage=StageGetCharacterInfo(hanziNetwork, structureManager)
		stage.execute()

		return stage.getCharacterInfoList()

