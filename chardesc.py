#!/usr/bin/env python3

import charinfo

class CharDesc:
	"""字符描述"""
	def __init__(self, name, description, chInfo):
		self.name=name

		self.op='龜'
		self.compList=[]

		self.description=description

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.chInfo=chInfo

	def setName(self, name):
		self.name=name

	def setOp(self, op):
		self.op=op

	def setCompList(self, compList):
		self.compList=compList

	def getCompList(self):
		return self.compList

	def getDescription(self):
		return self.getDescription

	def setChInfo(self, chInfo):
		self.chInfo=chInfo

	def getChInfo(self):
		return self.chInfo

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.name, self.op, ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

CharDesc.NoneDesc=CharDesc("", '', charinfo.CharInfo.NoneChar)

if __name__=='__main__':
	print(CharDesc.NoneDesc)
	print(CharDesc('王', '(龜)', None))

