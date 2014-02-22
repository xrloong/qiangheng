
import character.Operator as Operator
import character.OperatorManager

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
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='好'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		x=oldCompList[0]
		charDesc.setCompList([x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoH3:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='湘'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		x=oldCompList[0]
		charDesc.setCompList([x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoH4:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='膷'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		x=oldCompList[0]
		charDesc.setCompList([x, x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoV2:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='志'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		x=oldCompList[0]
		charDesc.setCompList([x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoV3:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='志'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		x=oldCompList[0]
		charDesc.setCompList([x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoV4:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='纂'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		x=oldCompList[0]
		charDesc.setCompList([x, x, x, x,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoTriangle:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='志'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		ansTmpOperatorName='好'
		ansTmpOperator=character.OperatorManager.getOperatorByName(ansTmpOperatorName)
		x=oldCompList[0]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, x,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoSquare:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='志'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		ansTmpOperatorName='好'
		ansTmpOperator=character.OperatorManager.getOperatorByName(ansTmpOperatorName)
		x=oldCompList[0]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, x,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([tmpDesc, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoSpecial:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='龍'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		x=oldCompList[0]
		y=oldCompList[1]

		if x.getName() in ['辶', '廴']:
			charDesc.setCompList([y, x])
			charDesc.setOperator(ansOperatorName)

class RearrangeInfoFrost:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='志'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		ansTmpOperatorName='好'
		ansTmpOperator=character.OperatorManager.getOperatorByName(ansTmpOperatorName)
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([y, z,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoThink:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='志'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		ansTmpOperatorName='好'
		ansTmpOperator=character.OperatorManager.getOperatorByName(ansTmpOperatorName)
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, y,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([tmpDesc, z,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoHappy:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='好'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		ansTmpOperatorName='志'
		ansTmpOperator=character.OperatorManager.getOperatorByName(ansTmpOperatorName)
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([y, z,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoSmart:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		ansOperatorName='好'
		ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
		ansTmpOperatorName='志'
		ansTmpOperator=character.OperatorManager.getOperatorByName(ansTmpOperatorName)
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, y,])
		tmpDesc.setOperator(ansTmpOperator)

		charDesc.setCompList([tmpDesc, z,])
		charDesc.setOperator(ansOperator)

class RearrangeInfoSurroundingOpenUp:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		if oldOperatorName=='函':
			ansOperatorName='龍'
			ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
			x=oldCompList[0]
			y=oldCompList[1]
			charDesc.setCompList([y, x])
			charDesc.setOperator(ansOperator)

class RearrangeInfoLShapeSimpleRadical:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldOperatorName=oldOperator.getName()
		oldCompList=charDesc.getCompList()

		if oldOperatorName=='起':
			ansOperatorName='龍'
			ansOperator=character.OperatorManager.getOperatorByName(ansOperatorName)
			x=oldCompList[0]
			y=oldCompList[1]

			if x.getName() in ['辶', '廴']:
				charDesc.setCompList([y, x])
				charDesc.setOperator(ansOperator)

