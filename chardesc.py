#!/usr/bin/env python3

class CharDesc:
	"""字符描述"""
	def __init__(self, name, description, chInfo):
		self.description='()'
		self.op='龜'
		self.compList=[]
		self.name=name
		self.description=description
		self.chInfo=chInfo

	def setName(self, name):
		self.name=name

	def setOp(self, op):
		self.op=op

	def setCompList(self, compList):
		self.compList=compList

	def getDescription(self):
		return self.getDescription

	def getChInfo(self):
		return self.chInfo

	def __str__(self):
		if self.name=="":
			return '<None>'
		else:
			return '<{0}={1}|({2})>'.format(self.name, self.op, ",".join(map(str, self.compList)))

CharDesc.NoneDesc=CharDesc("", '', None)

if __name__=='__main__':
	print(CharDesc.NoneDesc)
	print(CharDesc('王', '(龜)', None))

