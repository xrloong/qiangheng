from injector import inject

from .element import Operator

class OperatorManager:
	# 使用享元模式

	@inject
	def __init__(self):
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

	def generateOperator(self, operatorName):
		if operatorName in self.builtinOperatorDict:
			operator=self.builtinOperatorDict.get(operatorName)
		else:
			if operatorName not in self.templateOperatorDict:
				operator=Operator.Operator(operatorName)
				self.templateOperatorDict[operatorName]=operator
			operator=self.templateOperatorDict.get(operatorName)
		return operator

class RadixDescriptionManager:
	def __init__(self):
		self.descriptionDict={}
		self.radixCodeInfoDB={}
		self.resetRadixList=[]

	def addCodeInfoList(self, charName, radixCodeInfoList):
		self.radixCodeInfoDB[charName]=radixCodeInfoList

	def getResetRadixList(self):
		return self.resetRadixList

	def getCodeInfoDB(self):
		return self.radixCodeInfoDB

	def addDescription(self, charName, description):
		if description.isToOverridePrev():
			tmpRadixDesc = description
			self.resetRadixList.append(charName)
		else:
			if charName in self.descriptionDict:
				tmpRadixDesc=self.descriptionDict.get(charName)
				tmpRadixDesc.mergeRadixDescription(description)
			else:
				tmpRadixDesc=description

		self.descriptionDict[charName]=tmpRadixDesc

	def getDescriptionList(self):
		return list(self.descriptionDict.items())

