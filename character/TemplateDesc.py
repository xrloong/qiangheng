#!/usr/bin/env python3

import copy

class TemplateDesc:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, name, charDesc, parameterList):
		self.name=name

		self.charDesc=charDesc
		self.parameterList=parameterList

	def __str__(self):
		return '{0}({2})={1}'.format(self.name, self.charDesc, self.parameterList)

	def __repr__(self):
		return str(self)

	def setName(self, name):
		self.name=name

	def getName(self):
		return self.name

	def setParameterList(self, parameterList):
		self.parameterList=parameterList

	def getParameterList(self):
		return self.parameterList

	def getReplacedCharDesc(self, argumentList):
		argumentNameList=[charDesc.getName() for charDesc in argumentList]

		tempDesc=copy.deepcopy(self.charDesc)
		pairList=[]
		if len(argumentNameList)==len(self.parameterList):
			pairList=zip(self.parameterList, argumentNameList)

		mappingDict=dict(pairList)
		self.replaceCharDesc(tempDesc, mappingDict)
		return tempDesc

	def replaceCharDesc(self, charDesc, mappingDict):
		argumentName=mappingDict.get(charDesc.getName())
		if argumentName!=None:
			charDesc.setName(argumentName)

		for comp in charDesc.getCompList():
			self.replaceCharDesc(comp, mappingDict)

if __name__=='__main__':
	print(TemplateDesc('王', '(龜)', None))

