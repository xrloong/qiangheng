from .CharDesc import CharDesc
class RearrangementManager:
	def __init__(self, imModule, descMgr, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.imName=imModule.IMInfo.IMName
		self.descMgr=descMgr

	# 分成以下層級
	# SpecialCase:	錯、龜、水
	# 橫、縱：鴻：不定個數橫向組同，蚕：不定個數縱向組合，龍：不定個數的組同。
	# Base:		好、志、湘、算、纂、膷
	# Surrounding:	回、同、區、函、左
	# LShape:	廖、載、聖、起
	# Insertion:	夾、衍、衷
	# TowLayer:	霜、想、怡、穎
	# Repeate:	林、爻、卅、丰、卌、圭、燚
	def rearrangeDesc(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		self.rearrangeRepeate(charDesc)
		self.rearrangeTowLayer(charDesc)
		self.rearrangeInsertion(charDesc)
		self.rearrangeLShape(charDesc)
		self.rearrangeSpecialCase(charDesc)
		self.rearrangeSurrounding(charDesc)
		self.rearrangeBase(charDesc)

	def rearrangeSpecialCase(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='龜':
			pass
		elif oldOperator=='水':
			pass
		elif oldOperator=='錯':
			pass
		else:
			pass

	def rearrangeInsertion(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='夾':
			ansDirection='+'
		elif oldOperator=='衍':
			ansDirection='-'
			if self.imName!='鄭碼':
				x=oldCompList[0]
				y=oldCompList[1]

				leftDesc=self.descMgr.getExpandDescriptionByNameInNetwork('彳')
				rightDesc=self.descMgr.getExpandDescriptionByNameInNetwork('亍')
				if x.getName()=='行':
					charDesc.setCompList([leftDesc, y, rightDesc])
					charDesc.setOperatorAndDirection('湘', '-')
			else:
				pass
		elif oldOperator=='衷':
			ansDirection='|'
			x=oldCompList[0]
			y=oldCompList[1]

			upDesc=self.descMgr.getExpandDescriptionByNameInNetwork('亠')
			downDesc=self.descMgr.getExpandDescriptionByNameInNetwork('[衣下]')
			if x.getName()=='衣':
				charDesc.setCompList([upDesc, y, downDesc])
				charDesc.setOperatorAndDirection('志', '|')
		else:
			pass

	def rearrangeLShape(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='起':
			ansDirection='+'
			x=oldCompList[0]
			y=oldCompList[1]

#			if self.imName in ['嘸蝦米', '行列', '大易'] and x.getName()=='辶':
			if self.imName == '嘸蝦米' and x.getName() in ['辶', '廴']:
				charDesc.setCompList([y, x])
				charDesc.setOperatorAndDirection('龍', '+')
			elif self.imName == '行列' and x.getName() in ['辶', '廴']:
				charDesc.setCompList([y, x])
				charDesc.setOperatorAndDirection('龍', '+')
			elif self.imName == '大易' and x.getName() in ['辶', '廴']:
				charDesc.setCompList([y, x])
				charDesc.setOperatorAndDirection('龍', '+')
		elif oldOperator=='廖':
			ansDirection='+'
		elif oldOperator=='載':
			ansDirection='+'
		elif oldOperator=='聖':
			ansDirection='+'
		else:
			pass

	def rearrangeTowLayer(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='霜':
			ansDirection='|'
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]

			tmpDesc=self.emptyCharDescGenerator()
			tmpDesc.setCompList([y, z,])
			tmpDesc.setOperatorAndDirection('好', '-')

			charDesc.setCompList([x, tmpDesc,])
			charDesc.setOperatorAndDirection('志', ansDirection)
		elif oldOperator=='想':
			ansDirection='|'
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]

			tmpDesc=self.emptyCharDescGenerator()
			tmpDesc.setCompList([x, y,])
			tmpDesc.setOperatorAndDirection('好', '-')

			charDesc.setCompList([tmpDesc, z,])
			charDesc.setOperatorAndDirection('志', ansDirection)
		elif oldOperator=='怡':
			ansDirection='-'
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]

			tmpDesc=self.emptyCharDescGenerator()
			tmpDesc.setCompList([y, z,])
			tmpDesc.setOperatorAndDirection('志', '|')

			charDesc.setCompList([x, tmpDesc,])
			charDesc.setOperatorAndDirection('好', ansDirection)
		elif oldOperator=='穎':
			ansDirection='-'
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]

			tmpDesc=self.emptyCharDescGenerator()
			tmpDesc.setCompList([x, y,])
			tmpDesc.setOperatorAndDirection('志', '|')

			charDesc.setCompList([tmpDesc, z,])
			charDesc.setOperatorAndDirection('好', ansDirection)
		pass

	def rearrangeSurrounding(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='回':
			ansDirection='@'
		elif oldOperator=='同':
			ansDirection='@'
		elif oldOperator=='函':
			ansDirection='@'
		elif oldOperator=='區':
			ansDirection='@'
		elif oldOperator=='左':
			ansDirection='@'
		else:
			pass

	def rearrangeBase(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator=='好':
			ansDirection='-'
		elif oldOperator=='志':
			ansDirection='-'
		elif oldOperator=='算':
			ansDirection='|'
		elif oldOperator=='湘':
			ansDirection='-'
		elif oldOperator=='纂':
			ansDirection='|'
		elif oldOperator=='膷':
			ansDirection='-'
		else:
			pass

	def rearrangeRepeate(self, charDesc):
		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()
		if oldOperator=='林':
			ansDirection='-'
			x=oldCompList[0]
			charDesc.setCompList([x, x,])
			charDesc.setOperatorAndDirection('好', ansDirection)
		elif oldOperator=='爻':
			ansDirection='|'
			x=oldCompList[0]
			charDesc.setCompList([x, x,])
			charDesc.setOperatorAndDirection('志', ansDirection)
		elif oldOperator=='卅':
			ansDirection='-'
			x=oldCompList[0]
			charDesc.setCompList([x, x, x,])
			charDesc.setOperatorAndDirection('湘', ansDirection)
		elif oldOperator=='丰':
			ansDirection='|'
			x=oldCompList[0]
			charDesc.setCompList([x, x, x,])
			charDesc.setOperatorAndDirection('算', ansDirection)
		elif oldOperator=='鑫':
			ansDirection='|'
			x=oldCompList[0]

			tmpDesc=self.emptyCharDescGenerator()
			tmpDesc.setCompList([x, x,])
			tmpDesc.setOperatorAndDirection('好', '-')

			charDesc.setCompList([x, tmpDesc,])
			charDesc.setOperatorAndDirection('志', ansDirection)
		elif oldOperator=='卌':
			ansDirection='-'
			x=oldCompList[0]
			charDesc.setCompList([x, x, x, x,])
			charDesc.setOperatorAndDirection('膷', ansDirection)
		elif oldOperator=='圭':
			ansDirection='|'
			x=oldCompList[0]
			charDesc.setCompList([x, x, x, x,])
			charDesc.setOperatorAndDirection('纂', ansDirection)
		elif oldOperator=='燚':
			ansDirection='|'
			x=oldCompList[0]

			tmpDesc=self.emptyCharDescGenerator()
			tmpDesc.setCompList([x, x,])
			tmpDesc.setOperatorAndDirection('好', '-')

			charDesc.setCompList([tmpDesc, tmpDesc,])
			charDesc.setOperatorAndDirection('志', ansDirection)
		else:
			pass

	@staticmethod
	def computeDirection(oldOperator):
		"""計算部件的結合方向"""

		ansDir='+'
		if oldOperator in ['龜']:
			ansDir='+'
		elif oldOperator in ['龍']:
			ansDir='+'
		elif oldOperator in ['鴻']:
			ansDir='-'
		elif oldOperator in ['蚕']:
			ansDir='|'
		elif oldOperator in ['水']:
			# 暫時不會執行這段，且還在重構中
			pass
#			ansDir='+'
#			ansDir=self.getCompList()[0].getDirection()
		elif oldOperator in ['回', '同', '函', '區', '左']:
			ansDir='@'
		elif oldOperator in ['載', '廖', '起', '夾']:
			ansDir='+'
		elif oldOperator in ['纂', '算', '志', '霜', '想', '爻', '卅', ]:
			ansDir='|'
		elif oldOperator in ['湘', '好', '怡', '穎', '林', '鑫', ]:
			ansDir='-'
		elif oldOperator in ['燚',]:
			ansDir='+'
		else:
			ansDir='+'
		return ansDir


