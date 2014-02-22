#!/usr/bin/env python3

import sys
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

	def rearrange(self, charDesc):
		def getMapping(parameterList, argumentList):
			mappingDict={}
			if len(argumentList)==len(parameterList):
				pairList=zip(parameterList, argumentList)

				mappingDict=dict(pairList)
			else:
				print("參數列及引數列個數不符", file=sys.stderr)
			return mappingDict

		def getReplacedCharDesc(targetStructureDescription):
			tempDesc=targetStructureDescription.copyDeeply()

			replaceCharDesc(tempDesc)
			return tempDesc

		# 需要先替換兒子，才可以進行自己的替換。
		# 否則，如：條=(範翛 木)=(範湘 亻丨(志 夂木))
		# 而 '木' 會被誤判為湘的參數。
		def replaceCharDesc(charDesc):
			for comp in charDesc.getCompList():
				replaceCharDesc(comp)

			argumentDesc=mappingDict.get(charDesc.getExpandName())
			if argumentDesc!=None:
				charDesc.replacedBy(argumentDesc)

		def isConditionMatch(condition, mappingDict):
			if condition.isMatchAll():
				return True
			operand1=condition.getOperand1()
			operand2=condition.getOperand2()
			argumentDesc=mappingDict.get(operand1)
			return argumentDesc.getExpandName()==operand2

		def getWantedCharDesc(mappingDict):
			targetCharDesc=None
			for replaceInfo in self.replaceInfoList:
				[condition, charDesc]=replaceInfo
				if isConditionMatch(condition, mappingDict):
					targetCharDesc=charDesc
					break
			return targetCharDesc

		argumentList=charDesc.getCompList()
		parameterList=self.parameterList
		mappingDict=getMapping(parameterList, argumentList)
		targetStructureDescription=getWantedCharDesc(mappingDict)
		resultDesc=getReplacedCharDesc(targetStructureDescription)
		charDesc.replacedBy(resultDesc)

if __name__=='__main__':
	print(TemplateDescription('王', '(龜)', None))

