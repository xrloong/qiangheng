from im.gear import OperatorManager
from description.StructureDescription import HangerStructureDescription
from description.StructureDescription import StructureDescription
from im.gear import Operator
from gear import TreeRegExp

class StructureRearranger:
	def __init__(self):
		class TProxy(TreeRegExp.BasicTreeProxy):
			def __init__(self):
				pass

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
		self.treeProxy=TProxy()
		self.patternList=[(TreeRegExp.compile(re), result) for (re, result) in self.getPatternList()]

	def setOperatorGenerator(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

	def getOperatorGenerator(self):
		return self.operatorGenerator


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


	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription.generate(operator, CompList)
		return structDesc

	def generateStructureDescriptionWithName(self, name):
		structDesc=self.generateStructureDescription()
		structDesc.setReferenceExpression(name)
		return structDesc

	def rearrangeByTreeRegExp(self, structDesc):
		compList=structDesc.getCompList()
		for (tre, result) in self.patternList:
			matchResult=TreeRegExp.match(tre, structDesc, self.treeProxy)
			if matchResult.isMatched():
				tmpStructDesc=self.genStructDesc(tre, result)
				structDesc.setOperator(tmpStructDesc.getOperator())
				structDesc.setCompList(tmpStructDesc.getCompList())

	def generateTokens(self, expression):
		tokens=[]
		length=len(expression)
		i=0
		while i<length:
			if expression[i] in ["(", ")"]:
				tokens.append(expression[i])
				i+=1
			elif expression[i] == "\\":
				j=i+1
				while j<length and expression[j].isdigit():
					j+=1
				tokens.append(expression[i:j])
				i=j
			elif expression[i] == " ":
				i+=1
			else:
				j=i+1
				while j<length and expression[j] not in ["(", ")", "\\", " "]:
					j+=1
				tokens.append(expression[i:j])
				i=j
		return tokens

	def genStructDescRecursive(self, tre, tokens):
		if not tokens[0]=="(":
			return ([], None)
		operatorName = tokens[1]
		compList=[]
		rest=tokens[2:]
		while len(rest) > 0:
			if rest[0]=="(":
				rest, structDesc=self.genStructDescRecursive(tre, rest)
				if structDesc!=None:
					compList.append(structDesc)
			elif rest[0]==")":
				rest=rest[1:]
				break
			elif rest[0][:1]=="\\":
				index=int(rest[0][1:])
				rest=rest[1:]
				compList.extend(tre.getComp(index).getMatched())
			else:
				compList.append(self.generateStructureDescriptionWithName(rest[0]))
				rest=rest[1:]
		operator=self.operatorGenerator(operatorName)
		structDesc=StructureDescription.generate(operator, compList)
		return (rest, structDesc)

	def genStructDesc(self, tre, expression):
		return self.genStructDescRecursive(tre, self.generateTokens(expression))[1]

	def getPatternList(self):
		return []
