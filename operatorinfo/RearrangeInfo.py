
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

class RearrangeInfoGo:
	def __init__(self, descMgr, emptyCharDescGenerator):
		self.descMgr=descMgr
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='衍':
			ansDirection='-'
			x=oldCompList[0]
			y=oldCompList[1]

			leftDesc=self.descMgr.getExpandDescriptionByNameInNetwork('彳')
			rightDesc=self.descMgr.getExpandDescriptionByNameInNetwork('亍')
			if x.getName()=='行':
				charDesc.setCompList([leftDesc, y, rightDesc])
				charDesc.setOperatorAndDirection('湘', '-')

class RearrangeInfoHeart:
	def __init__(self, descMgr, emptyCharDescGenerator):
		self.descMgr=descMgr
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='衷':
			ansDirection='|'
			x=oldCompList[0]
			y=oldCompList[1]

			upDesc=self.descMgr.getExpandDescriptionByNameInNetwork('亠')
			downDesc=self.descMgr.getExpandDescriptionByNameInNetwork('[衣下]')
			if x.getName()=='衣':
				charDesc.setCompList([upDesc, y, downDesc])
				charDesc.setOperatorAndDirection('志', '|')

class RearrangeInfoSpecial:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		ansDirection='+'
		x=oldCompList[0]
		y=oldCompList[1]

		if x.getName() in ['辶', '廴']:
			charDesc.setCompList([y, x])
			charDesc.setOperatorAndDirection('龍', '+')

class RearrangeInfoFrost:
	def __init__(self):
		pass

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

		ansDirection='+'
		if oldOperator=='起':
			ansDirection='+'
			x=oldCompList[0]
			y=oldCompList[1]

			if x.getName() in ['辶', '廴']:
				charDesc.setCompList([y, x])
				charDesc.setOperatorAndDirection('龍', '+')

RearrangeInfo.Order_01=RearrangeInfo([0, 1,])
RearrangeInfo.Order_10=RearrangeInfo([1, 0,])
RearrangeInfo.Order_012=RearrangeInfo([0, 1, 2])

