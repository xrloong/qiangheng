
class RearrangeInfo:
	def __init__(self, order):
		sameOrder=range(len(order))
		if sorted(order)==sameOrder:
			self.indexOrder=order
		else:
			self.indexOrder=sameOrder

	def rearrange(self, charDesc):
		pass

#	def rearrange(self, oldList):
#		newList=[]
#		for index in self.indexOrder:
#			newList.append(oldList[index])
#		return newList

class RearrangeInfoSame:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		pass

class RearrangeInfoSurroundingOpenUp:
	def __init__(self, OperatorLoong):
		self.operatorLoong=OperatorLoong

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorLoong
		x=oldCompList[0]
		y=oldCompList[1]
		charDesc.setCompList([y, x])
		charDesc.setOperator(ansOperator)

class RearrangeInfoLShapeSimpleRadical:
	def __init__(self, OperatorLoong):
		self.operatorLoong=OperatorLoong

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorLoong
		x=oldCompList[0]
		y=oldCompList[1]

		if x.getName() in ['辶', '廴']:
			charDesc.setCompList([y, x])
			charDesc.setOperator(ansOperator)

