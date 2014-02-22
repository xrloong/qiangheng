
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

class RearrangeInfoH2:
	def __init__(self, OperatorH2):
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorH2
		x=oldCompList[0]
		charDesc.setCompList([x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoH3:
	def __init__(self, OperatorH3):
		self.operatorH3=OperatorH3

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorH3
		x=oldCompList[0]
		charDesc.setCompList([x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoH4:
	def __init__(self, OperatorH4):
		self.operatorH4=OperatorH4

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorH4
		x=oldCompList[0]
		charDesc.setCompList([x, x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoV2:
	def __init__(self, OperatorV2):
		self.operatorV2=OperatorV2

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorV2
		x=oldCompList[0]
		charDesc.setCompList([x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoV3:
	def __init__(self, OperatorV3):
		self.operatorV3=OperatorV3

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorV3
		x=oldCompList[0]
		charDesc.setCompList([x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoV4:
	def __init__(self, OperatorV4):
		self.operatorV4=OperatorV4

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorV4
		x=oldCompList[0]
		charDesc.setCompList([x, x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoTriangle:
	def __init__(self, emptyCharDescGenerator, OperatorH2, OperatorV2):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.operatorV2=OperatorV2
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorV2
		ansTmpOperator=self.operatorH2
		x=oldCompList[0]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, x,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoSquare:
	def __init__(self, emptyCharDescGenerator, OperatorH2, OperatorV2):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.operatorV2=OperatorV2
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorV2
		ansTmpOperator=self.operatorH2
		x=oldCompList[0]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, x,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([tmpDesc, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoFrost:
	def __init__(self, emptyCharDescGenerator, OperatorH2, OperatorV2):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.operatorV2=OperatorV2
		self.operatorH2=OperatorH2

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
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
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
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
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
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
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
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
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
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
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorLoong
		x=oldCompList[0]
		y=oldCompList[1]

		if x.getName() in ['辶', '廴']:
			charDesc.setCompList([y, x])
			charDesc.setOperator(ansOperator)

