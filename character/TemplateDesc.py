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
		tempDesc=self.charDesc.copyDeeply()
		tempDesc.setExpandName(self.charDesc.getExpandName())
		mappingDict={}
		if len(argumentList)==len(self.parameterList):
			pairList=zip(self.parameterList, argumentList)

			mappingDict=dict(pairList)
		self.replaceCharDesc(tempDesc, mappingDict)
		return tempDesc

	# 需要先替換兒子，才可以進行自己的替換。
	# 否則，如：條=(範翛 木)=(範湘 亻丨(志 夂木))
	# 而 '木' 會被誤判為湘的參數。
	def replaceCharDesc(self, charDesc, mappingDict):
		for comp in charDesc.getCompList():
			self.replaceCharDesc(comp, mappingDict)

		argumentDesc=mappingDict.get(charDesc.getExpandName())
		if argumentDesc!=None:
			argumentName=argumentDesc.getExpandName()
			charDesc.setHanger(argumentDesc.getHanger().copyDeeply())
			charDesc.setExpandName(argumentName)

if __name__=='__main__':
	print(TemplateDesc('王', '(龜)', None))

