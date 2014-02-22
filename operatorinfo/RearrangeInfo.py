
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

class RearrangeInfoFrost:
	def __init__(self, emptyCharDescGenerator, OperatorH2, OperatorV2):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.operatorV2=OperatorV2
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorV2
		ansTmpOperator=self.operatorH2
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([y, z,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoThink:
	def __init__(self, emptyCharDescGenerator, OperatorH2, OperatorV2):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.operatorV2=OperatorV2
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorV2
		ansTmpOperator=self.operatorH2
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, y,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([tmpDesc, z,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoHappy:
	def __init__(self, emptyCharDescGenerator, OperatorH2, OperatorV2):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.operatorV2=OperatorV2
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorH2
		ansTmpOperator=self.operatorV2
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([y, z,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoSmart:
	def __init__(self, emptyCharDescGenerator, OperatorH2, OperatorV2):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.operatorV2=OperatorV2
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorH2
		ansTmpOperator=self.operatorV2
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, y,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([tmpDesc, z,])
		charDesc.setOperator(ansOperator)

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

