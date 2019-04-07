from injector import inject

from . import TreeRegExp
from ..hanzi import HanZiNetwork
from model.interpreter import CodeInfoInterpreter
from model.manager import OperatorManager
from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import RadixManager

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
	def __init__(self, codeInfoInterpreter):
		super().__init__()
		self.codeInfoInterpreter = codeInfoInterpreter

	def setInfoListList(self, operator, infoListList):
		codeInfoList=[]
		for infoList in infoListList:
			codeInfo = self.codeInfoInterpreter.encodeToCodeInfo(operator, infoList)
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


class TreeProxyOfStageAddStructure(TreeRegExp.BasicTreeProxy):
	def __init__(self, hanziNetwork, stage, operationManager):
		self.operationManager = operationManager
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
		operator=self.operationManager.generateOperator(operatorName)
		structure = self.stage.generateAssemblageStructure(operator, children)
		return structure


class TaskAddNode:
	# 加入如 "相" "[漢右]" 的節點。
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork, radixManager: RadixManager):
		self.hanziNetwork = hanziNetwork
		self.radixManager = radixManager

	def handleCharacter(self, character):
		from model.element import CharacterInfo

		characterInfo=CharacterInfo.CharacterInfo(character)
		self.hanziNetwork.addNode(character, characterInfo)

		if self.radixManager.hasRadix(character):
			radixInfoList=self.radixManager.getRadixCodeInfoList(character)
			for radixCodeInfo in radixInfoList:
				structure=self.generateUnitLink(radixCodeInfo)
				self.hanziNetwork.addUnitStructureIntoNode(structure, character)

	def generateUnitLink(self, radixCodeInfo):
		tag=StructureUnitTag(radixCodeInfo)
		structure=self.hanziNetwork.generateStructure(tag)
		return structure

class TaskAddStructure:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork, structureManager: StructureManager,
			operationManager: OperatorManager,
			codeInfoInterpreter: CodeInfoInterpreter):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager
		self.codeInfoInterpreter = codeInfoInterpreter
		self.treeProxy=TreeProxyOfStageAddStructure(hanziNetwork, self, operationManager)
		self.nodeExpressionDict={}

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

	def generateAssemblageStructure(self, operator, structureList):
		tag=StructureAssemblageTag(self.codeInfoInterpreter)
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

class TaskSetNodeTree:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork, structureManager: StructureManager):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager

	def handleCharacter(self, character):
		node=self.hanziNetwork.findNode(character)
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

class TaskGetCharacterInfo:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork, structureManager: StructureManager,
			codeInfoInterpreter: CodeInfoInterpreter):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager
		self.codeInfoInterpreter = codeInfoInterpreter
		self.characterInfoList=[]

	def handleCharacter(self, character):
		characterInfo=None

		charNode=self.hanziNetwork.findNode(character)
		if charNode:
			characterInfo=self.getNodeCharacterInfo(charNode)

		if characterInfo:
			return characterInfo

	def getCharacterInfoList(self):
		return self.characterInfoList

	def getNodeCharacterInfo(self, hanziNode):
		structureList=hanziNode.getStructureList(True)
		codeInfoList=sum(map(lambda s: s.getTag().getCodeInfoList(), structureList), [])
		codeInfoList=filter(lambda x: x.isSupportCharacterCode(), codeInfoList)

		codeList=self.codeInfoInterpreter.interpretCodeInfoList(codeInfoList)

		characterInfo=hanziNode.getTag()
		characterInfo.setCodeList(codeList)

		return characterInfo

class ComputeCharacterInfo:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork, structureManager: StructureManager,
			taskAddNode: TaskAddNode,
			taskAddStructure: TaskAddStructure,
			taskSetNodeTree: TaskSetNodeTree,
			taskGetCharacterInfo: TaskGetCharacterInfo,
			):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager

		self.taskAddNode = taskAddNode
		self.taskAddStructure = taskAddStructure
		self.taskSetNodeTree = taskSetNodeTree
		self.taskGetCharacterInfo = taskGetCharacterInfo

	def compute(self, characterSet = None):
		characterSet = characterSet if characterSet != None else self.structureManager.getAllCharacters()
		characters = self.structureManager.getAllCharacters()
		for character in characters:
			self.taskAddNode.handleCharacter(character)
		for character in characters:
			self.taskAddStructure.handleCharacter(character)
		for character in characters:
			self.taskSetNodeTree.handleCharacter(character)

		characterInfoList=[]
		for character in characterSet:
			characterInfo = self.taskGetCharacterInfo.handleCharacter(character)

			if characterInfo:
				characterInfoList.append(characterInfo)
		return characterInfoList

