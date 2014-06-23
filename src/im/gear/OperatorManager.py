from . import Operator
from . import RearrangeInfo
from parser import QHParser
from description.StructureDescription import HangerStructureDescription
from description.StructureDescription import StructureDescription
from gear import TreeRegExp
import yaml

class OperatorManager:
	# 使用享元模式

	def __init__(self, imPackage):
		self.builtinOperatorDict={
			'龜':Operator.OperatorTurtle,
			'爲':Operator.OperatorEqual,
			'龍':Operator.OperatorLoong,
			'雀':Operator.OperatorSparrow,
			'蚕':Operator.OperatorSilkworm,
			'鴻':Operator.OperatorGoose,
			'回':Operator.OperatorLoop,

			'起':Operator.OperatorQi,
			'廖':Operator.OperatorLiao,
			'載':Operator.OperatorZai,
			'斗':Operator.OperatorDou,

			'同':Operator.OperatorTong,
			'函':Operator.OperatorHan,
			'區':Operator.OperatorQu,
			'左':Operator.OperatorLeft,

			'衍':Operator.OperatorYan,
			'衷':Operator.OperatorZhong,
			'瓥':Operator.OperatorLi,
			'粦':Operator.OperatorLin,

			'畞':Operator.OperatorMu,
			'㘴':Operator.OperatorZuo,
			'幽':Operator.OperatorYou,
			'㒳':Operator.OperatorLiang,
			'夾':Operator.OperatorJia,

			'燚':Operator.OperatorYi,
		}
		self.templateOperatorDict={
		}

		def operatorGenerator(operatorName):
			if operatorName in self.builtinOperatorDict:
				operator=self.builtinOperatorDict.get(operatorName)
			else:
				self.addTemplateOperatorIfNotExist(operatorName)
				operator=self.findTemplateOperator(operatorName)
			return operator

		self.operatorGenerator=operatorGenerator
		self.structureRearranger=StructureRearranger(operatorGenerator)

	def addTemplateOperatorIfNotExist(self, templateName):
		if templateName in self.templateOperatorDict:
			operator=self.templateOperatorDict[templateName]
		else:
			operator=Operator.TemplateOperator(templateName)
			self.templateOperatorDict[templateName]=operator

	def findTemplateOperator(self, templateName):
		templateOperator=self.templateOperatorDict.get(templateName)
		return templateOperator

	def setTemplateDB(self, templateDB):
		for templateName, templateDesc in templateDB.items():
			rearrangeInfoTemplate=RearrangeInfo.RearrangeInfoTemplate(templateDesc)

			self.addTemplateOperatorIfNotExist(templateName)
			templateOperator=self.findTemplateOperator(templateName)
			templateOperator.setRearrangeInfo(rearrangeInfoTemplate)

	def getOperatorGenerator(self):
		return self.operatorGenerator

	def rearrangeStructure(self, structDesc):
		self.structureRearranger.rearrangeOn(structDesc)

	def loadTemplate(self, toTemplateList):
		parser=QHParser.QHParser(self.operatorGenerator)
		templateDB={}
		for filename in toTemplateList:
			tmpTemplateDB=parser.loadTemplates(filename)
			templateDB.update(tmpTemplateDB)

		self.setTemplateDB(templateDB)

	def loadSubstituteRules(self, toSubstituteFile):
		self.structureRearranger.loadSubstituteRules(toSubstituteFile)

class TProxy(TreeRegExp.BasicTreeProxy):
	def __init__(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

	def getChildren(self, tree):
		return tree.getCompList()

	def matchSingle(self, tre, tree):
		prop=tre.prop
		isMatch = True
		if "名稱" in prop:
			isMatch &= prop.get("名稱") == tree.getReferenceExpression()

		if "運算" in prop:
			isMatch &= prop.get("運算") == tree.getOperator().getName()

		return isMatch

	def generateLeafNode(self, nodeName):
		return self.generateStructureDescriptionWithName(nodeName)

	def generateNode(self, operatorName, children):
		operator=self.operatorGenerator(operatorName)
		structDesc=StructureDescription.generate(operator, children)
		return structDesc

	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription.generate(operator, CompList)
		return structDesc

	def generateStructureDescriptionWithName(self, name):
		structDesc=self.generateStructureDescription()
		structDesc.setReferenceExpression(name)
		return structDesc


class StructureRearranger:
	def __init__(self, operatorGenerator):
		self.treeProxy=TProxy(operatorGenerator)
		self.patternList=[(TreeRegExp.compile(re), result) for (re, result) in self.getPatternList()]

	def loadSubstituteRules(self, toSubstituteFile):
		rootNode=yaml.load(open(toSubstituteFile))
		ruleSetNode=rootNode.get("規則集")
		self.patternList=[]
		for node in ruleSetNode:
			matchPattern=node.get("比對")
			resultPattern=node.get("替換")
			self.patternList.append([TreeRegExp.compile(matchPattern), resultPattern])

	def rearrangeOn(self, structDesc):
		self.rearrangeRecursively(structDesc)

	def rearrangeRecursively(self, structDesc):
		self.rearrangeDesc(structDesc)
		for childDesc in structDesc.getCompList():
			self.rearrangeRecursively(childDesc)
		return structDesc

	def rearrangeDesc(self, structDesc):
		self.rearrangeByTreeRegExp(structDesc)

		operator=structDesc.getOperator()
		while not operator.isBuiltin():
			rearrangeInfo=operator.getRearrangeInfo()

			if rearrangeInfo!=None:
				rearrangeInfo.rearrange(structDesc)
				self.rearrangeDesc(structDesc)
				operator=structDesc.getOperator()
			else:
				break


	def rearrangeByTreeRegExp(self, structDesc):
		compList=structDesc.getCompList()
		for (tre, result) in self.patternList:
			tmpStructDesc=TreeRegExp.matchAndReplace(tre, structDesc, result, self.treeProxy)
			if tmpStructDesc!=None:
				structDesc.setOperator(tmpStructDesc.getOperator())
				structDesc.setCompList(tmpStructDesc.getCompList())

	def getPatternList(self):
		return []
