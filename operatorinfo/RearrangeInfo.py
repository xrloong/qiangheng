
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
		oldCompList=charDesc.getCompList()

		ansDirection='-'
		x=oldCompList[0]
		charDesc.setCompList([x, x,])
		charDesc.setOperatorAndDirection('好', ansDirection)

class RearrangeInfoH3:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='-'
		x=oldCompList[0]
		charDesc.setCompList([x, x, x,])
		charDesc.setOperatorAndDirection('湘', ansDirection)

class RearrangeInfoH4:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='-'
		x=oldCompList[0]
		charDesc.setCompList([x, x, x, x,])
		charDesc.setOperatorAndDirection('膷', ansDirection)

class RearrangeInfoV2:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='|'
		x=oldCompList[0]
		charDesc.setCompList([x, x,])
		charDesc.setOperatorAndDirection('志', ansDirection)

class RearrangeInfoV3:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='|'
		x=oldCompList[0]
		charDesc.setCompList([x, x, x,])
		charDesc.setOperatorAndDirection('志', ansDirection)

class RearrangeInfoV4:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='|'
		x=oldCompList[0]
		charDesc.setCompList([x, x, x, x,])
		charDesc.setOperatorAndDirection('纂', ansDirection)

class RearrangeInfoTriangle:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='|'
		x=oldCompList[0]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, x,])
		tmpDesc.setOperatorAndDirection('好', '-')

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperatorAndDirection('志', ansDirection)

class RearrangeInfoSquare:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='|'
		x=oldCompList[0]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, x,])
		tmpDesc.setOperatorAndDirection('好', '-')

		charDesc.setCompList([tmpDesc, tmpDesc,])
		charDesc.setOperatorAndDirection('志', ansDirection)

class RearrangeInfoSpecial:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='*'
		x=oldCompList[0]
		y=oldCompList[1]

		if x.getName() in ['辶', '廴']:
			charDesc.setCompList([y, x])
			charDesc.setOperatorAndDirection('龍', '*')

class RearrangeInfoFrost:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='|'
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([y, z,])
		tmpDesc.setOperatorAndDirection('好', '-')

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperatorAndDirection('志', ansDirection)

class RearrangeInfoThink:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='|'
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, y,])
		tmpDesc.setOperatorAndDirection('好', '-')

		charDesc.setCompList([tmpDesc, z,])
		charDesc.setOperatorAndDirection('志', ansDirection)

class RearrangeInfoHappy:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='-'
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([y, z,])
		tmpDesc.setOperatorAndDirection('志', '|')

		charDesc.setCompList([x, tmpDesc,])
		charDesc.setOperatorAndDirection('好', ansDirection)

class RearrangeInfoSmart:
	def __init__(self, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='-'
		x=oldCompList[0]
		y=oldCompList[1]
		z=oldCompList[2]

		tmpDesc=self.emptyCharDescGenerator()
		tmpDesc.setCompList([x, y,])
		tmpDesc.setOperatorAndDirection('志', '|')

		charDesc.setCompList([tmpDesc, z,])
		charDesc.setOperatorAndDirection('好', ansDirection)

class RearrangeInfoSurroundingOpenUp:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='函':
			ansDirection='@'
			x=oldCompList[0]
			y=oldCompList[1]
			charDesc.setCompList([y, x])
			charDesc.setOperatorAndDirection('龍', '@')

class RearrangeInfoLShapeSimpleRadical:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='*'
		if oldOperator=='起':
			ansDirection='*'
			x=oldCompList[0]
			y=oldCompList[1]

			if x.getName() in ['辶', '廴']:
				charDesc.setCompList([y, x])
				charDesc.setOperatorAndDirection('龍', '*')

