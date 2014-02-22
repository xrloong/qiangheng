#!/usr/bin/env python3

import copy

class TemplateCondition:
	def __init__(self, expression=[None, None, None]):
		operator, operand1, operand2=expression

		self.operator=operator
		self.operand1=operand1
		self.operand2=operand2

	def isMatchAll(self):
		return self.operator==None

	def getOperand1(self):
		return self.operand1

	def getOperand2(self):
		return self.operand2

class TemplateDescription:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, name, parameterList, replaceInfoList):
		self.name=name

		[condition, charDesc]=replaceInfoList[0]

		self.charDesc=charDesc
		self.replaceInfoList=replaceInfoList
		self.parameterList=parameterList

	def __str__(self):
		return '{0}({2})={1}'.format(self.name, self.charDesc, self.parameterList)

	def __repr__(self):
		return str(self)

#	def setName(self, name):
#		self.name=name

	def getName(self):
		return self.name

	def setParameterList(self, parameterList):
		self.parameterList=parameterList

#	def getParameterList(self):
#		return self.parameterList

	def getWantedCharDesc(self, mappingDict):
		def isConditionMatch(condition, mappingDict):
			if condition.isMatchAll():
				return True
			operand1=condition.getOperand1()
			operand2=condition.getOperand2()
			argumentDesc=mappingDict.get(operand1)
			return argumentDesc.getExpandName()==operand2

		targetCharDesc=None
		for replaceInfo in self.replaceInfoList:
			[condition, charDesc]=replaceInfo
			if isConditionMatch(condition, mappingDict):
				targetCharDesc=charDesc
				break
		return targetCharDesc

	def getReplacedCharDesc(self, argumentList):
		mappingDict={}
		if len(argumentList)==len(self.parameterList):
			pairList=zip(self.parameterList, argumentList)

			mappingDict=dict(pairList)

		targetCharDesc=self.getWantedCharDesc(mappingDict)
		tempDesc=targetCharDesc.copyDeeply()

		self.replaceCharDesc(tempDesc, mappingDict)
		return tempDesc

	def rearrange(self, charDesc):
		compList=charDesc.getCompList()
		resultDesc=self.getReplacedCharDesc(compList)
		charDesc.replacedBy(resultDesc)

	# 需要先替換兒子，才可以進行自己的替換。
	# 否則，如：條=(範翛 木)=(範湘 亻丨(志 夂木))
	# 而 '木' 會被誤判為湘的參數。
	def replaceCharDesc(self, charDesc, mappingDict):
		for comp in charDesc.getCompList():
			self.replaceCharDesc(comp, mappingDict)

		argumentDesc=mappingDict.get(charDesc.getExpandName())
		if argumentDesc!=None:
			charDesc.replacedBy(argumentDesc)

if __name__=='__main__':
	print(TemplateDescription('王', '(龜)', None))

