from im.gear import OperatorManager
from description.StructureDescription import HangerStructureDescription
from im.gear import Operator

class StructureRearranger:
	def __init__(self):
		pass

	def setOperatorGenerator(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

	def getOperatorGenerator(self):
		return self.operatorGenerator


	def rearrangeOn(self, charDesc):
		structDescList=charDesc.getStructureList()
		for structDesc in structDescList:
			self.rearrangeRecursively(structDesc)

	def rearrangeRecursively(self, structDesc):
		self.rearrangeDesc(structDesc)
		for childDesc in structDesc.getCompList():
			self.rearrangeRecursively(childDesc)
		return structDesc

	def rearrangeDesc(self, structDesc):
		if self.rearrangeSpecial(structDesc):
			pass
		else:
			operator=structDesc.getOperator()
			if not operator.isBuiltin():
				rearrangeInfo=operator.getRearrangeInfo()

				if rearrangeInfo!=None:
					rearrangeInfo.rearrange(structDesc)
					operator=structDesc.getOperator()
					self.rearrangeDesc(structDesc)

	def rearrangeSpecial(self, structDesc):
		return False



	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription(operator, CompList)
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

