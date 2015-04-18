import Constant

from . import Operator
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

		self.templatePatternDict={
		}

		self.treeProxy=TProxy()
		self.substitutePatternList=[]

	def generateOperatorTurtle(self):
		return self.generateOperator()

	def generateOperator(self, operatorName):
		if operatorName in self.builtinOperatorDict:
			operator=self.builtinOperatorDict.get(operatorName)
		else:
			self.addTemplateOperatorIfNotExist(operatorName)
			operator=self.findTemplateOperator(operatorName)
		return operator

	def addTemplateOperatorIfNotExist(self, templateName):
		if templateName not in self.templateOperatorDict:
			operator=Operator.Operator(templateName)
			self.templateOperatorDict[templateName]=operator

	def findTemplateOperator(self, templateName):
		templateOperator=self.templateOperatorDict.get(templateName)
		return templateOperator

	def loadTemplates(self, toTemplateFile):
		node=yaml.load(open(toTemplateFile), yaml.CLoader)
		templatePatternDict={}
		templateGroupNode=node.get(Constant.TAG_TEMPLATE_SET)
		for node in templateGroupNode:
			templateName=node.get(Constant.TAG_NAME)
			matchPattern=node.get(Constant.TAG_MATCH)
			replacePattern=node.get(Constant.TAG_PATTERN)
			tre=TreeRegExp.compile(matchPattern)

			templatePatternDict[templateName]=[tre, replacePattern]

		self.templatePatternDict=templatePatternDict

	def loadSubstituteRules(self, toSubstituteFile):
		rootNode=yaml.load(open(toSubstituteFile))
		ruleSetNode=rootNode.get(Constant.TAG_RULE_SET)
		self.substitutePatternList=[]

		if not ruleSetNode:
			return

		for node in ruleSetNode:
			matchPattern=node.get(Constant.TAG_MATCH)
			resultPattern=node.get(Constant.TAG_SUBSTITUTE)
			self.substitutePatternList.append([TreeRegExp.compile(matchPattern), resultPattern])

	def getTemplatePatternList(self):
		return list(self.templatePatternDict.values())

	def getSubstitutePatternList(self):
		return self.substitutePatternList

	def rearrangeStructureSingleLevel(self, structDesc):
		self.rearrangeDesc(structDesc)

	def rearrangeDesc(self, structDesc):
		operator=structDesc.getOperator()
		while not operator.isBuiltin():
			templateName=operator.getName()

			if templateName not in self.templatePatternDict:
				break

			[tre, replacePattern,]=self.templatePatternDict[templateName]

			r=self.rearrangeByTreeRegExp(structDesc, [tre, replacePattern, ])
			if not r: break
			self.rearrangeDesc(structDesc)
			operator=structDesc.getOperator()

	def rearrangeByTreeRegExp(self, structDesc, pattern):
		(tre, result)=pattern
		tmpStructDesc=TreeRegExp.matchAndReplace(tre, structDesc, result, self.treeProxy)
		if tmpStructDesc!=None:
			structDesc.setOperator(tmpStructDesc.getOperator())
			structDesc.setCompList(tmpStructDesc.getCompList())
			return True
		return False

class TProxy(TreeRegExp.BasicTreeProxy):
	def __init__(self):
		from description.StructureDescription import StructureDescription
		self.structureGenerator=StructureDescription.Generator()

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

	def generateLeafNode(self, nodeExpression):
		return self.structureGenerator.generateLeafNode(nodeExpression)

	def generateLeafNodeByReference(self, referencedNode, index):
		nodeExpression="%s.%d"%(referencedNode.getReferenceName(), index)
		return self.generateLeafNode(nodeExpression)

	def generateNode(self, operatorName, children):
		return self.structureGenerator.generateNode([operatorName, children])

