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
		self.rearrangeSpecial(structDesc)

		operator=structDesc.getOperator()
		while not operator.isBuiltin():
			rearrangeInfo=operator.getRearrangeInfo()

			if rearrangeInfo!=None:
				rearrangeInfo.rearrange(structDesc)
				self.rearrangeDesc(structDesc)
				operator=structDesc.getOperator()
			else:
				break

	def rearrangeSpecial(self, structDesc):
		pass



	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription.generate(operator, CompList)
		return structDesc

	def generateStructureDescriptionWithName(self, name):
		structDesc=self.generateStructureDescription()
		structDesc.setReferenceExpression(name)
		return structDesc


	def getRearrangeListSilkworm(self):
		# 蚕
		rearrangeList=[
			# 範例
#			['一', '口', ['[一口]']],
			]
		return rearrangeList

	def getRearrangeListZai(self):
		# 載
		rearrangeList=[
			# 範例
#			['戈', '口', ['[一口]', '[特戈]']],
			]
		return rearrangeList

	def getRearrangeListFanFu(self):
		# 範焤
		rearrangeList=[
			'厭', '辰', '麻'
			]
		return rearrangeList

	def getRearrangeListFanYan(self):
		# 範衍
		rearrangeList=[
			# 範例
#			['儿.0', '儿.1', ['丨', '乚']],
#			['儿.0', '儿.1', '儿'],
			]
		return rearrangeList


	def rearrangeForSilkworm(self, structDesc):
		compList=structDesc.getCompList()

		rearrangeList=self.getRearrangeListSilkworm()

		newCompList=compList
		for [firstName, secondName, resultList] in rearrangeList:
			compList=newCompList
			newCompList=[]

			firstChildStructDesc=None
			secondChildStructDesc=compList[0]
			for idx in range(1, len(compList)):
				firstChildStructDesc=secondChildStructDesc
				secondChildStructDesc=compList[idx]

				if firstChildStructDesc==None or secondChildStructDesc==None:
					continue

				isMatch= firstChildStructDesc.getReferenceExpression()==firstName \
					and secondChildStructDesc.getReferenceExpression()==secondName
				if isMatch:
					for resultName in resultList:
						newStructDesc=self.generateStructureDescriptionWithName(resultName)
						newCompList.append(newStructDesc)
					firstChildStructDesc=None
					secondChildStructDesc=None
				else:
					newCompList.append(firstChildStructDesc)
			if secondChildStructDesc!=None:
				newCompList.append(secondChildStructDesc)

				structDescList=newCompList
				structDesc.setCompList(structDescList)
				structDesc.setOperator(Operator.OperatorSilkworm)

	def rearrangeForZai(self, structDesc):
		compList=structDesc.getCompList()

		rearrangeList=self.getRearrangeListZai()

		newCompList=compList
		for [firstName, secondName, resultList] in rearrangeList:
			firstChildStructDesc=compList[0]
			secondChildStructDesc=compList[1]
			isMatch= firstChildStructDesc.getReferenceExpression()==firstName \
				and secondChildStructDesc.getReferenceExpression()==secondName
			if isMatch:
				rearName=resultList[-1]
				newCompList=[]
				for frontName in resultList[:-1]:
					newFrontStructDesc=self.generateStructureDescriptionWithName(frontName)
					newCompList.append(newFrontStructDesc)
				newRearStructDesc=self.generateStructureDescriptionWithName(rearName)
				newCompList.extend(compList[1:-1])
				newCompList.append(newRearStructDesc)

				structDescList=newCompList
				structDesc.setCompList(structDescList)
				structDesc.setOperator(Operator.OperatorLoong)

	def rearrangeForFanFu(self, structDesc):
		compList=structDesc.getCompList()
		childStructDesc=compList[0]

		rearrangeList=self.getRearrangeListFanFu()
		if childStructDesc.getReferenceExpression() in rearrangeList:
			structDesc.setOperator(Operator.OperatorLiao)

	def rearrangeForFanYan(self, structDesc):
		compList=structDesc.getCompList()

		firstChhildStructDesc=compList[0]
		lastChildStructDesc=compList[-1]

		rearrangeList=self.getRearrangeListFanYan()
		for [leftName, rightName, result] in rearrangeList:
			isMatch= firstChhildStructDesc.getReferenceExpression()==leftName \
				and lastChildStructDesc.getReferenceExpression()==rightName
			if isMatch:
				if type(result) is type([]):
					[newLeftName, newRightName]=result
					newLeftStructDesc=self.generateStructureDescriptionWithName(newLeftName)
					newRightStructDesc=self.generateStructureDescriptionWithName(newRightName)
					structDescList=[newLeftStructDesc]+compList[1:-1]+[newRightStructDesc]
				else:
					resultName=result
					newStructDesc=self.generateStructureDescriptionWithName(resultName)
					structDescList=[newStructDesc]+compList[1:-1]

				structDesc.setCompList(structDescList)
				structDesc.setOperator(Operator.OperatorGoose)

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
		expression=expression[1:-1]
		expressionList=expression.split()
		operatorName=expressionList[0]

		compList=[self.generateStructureDescriptionWithName(expression) for expression in expressionList[1:]]

		compList=[]
		for expression in expressionList[1:]:
			if expression[:1]=='\\':
				index=int(expression[1:])
				compList.extend(tre.getComp(index).getMatched())
			else:
				compList.append(self.generateStructureDescriptionWithName(expression))

		operator=self.operatorGenerator(operatorName)
		structureDescription=StructureDescription.generate(operator, compList)
		return structureDescription

	def genStructDesc(self, tre, expression):
		return self.genStructDescRecursive(tre, self.generateTokens(expression))[1]

	def getPatternList(self):
		return []
