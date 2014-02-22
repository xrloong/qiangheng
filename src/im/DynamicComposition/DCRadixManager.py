from .DCCodeInfo import DCCodeInfo
from .DCCodeInfoEncoder import DCCodeInfoEncoder
from ..base.RadixManager import RadixParser
from .Calligraphy import Pane
from .Calligraphy import Stroke
from .Calligraphy import StrokeAction
from .Calligraphy import StrokeGroup
import re

class StrokeObject:
	def __init__(self, name, scope, expression):
		self.name = name
		self.scope = scope
		self.expression = expression
		self.scopeWidth = scope[2]-scope[0]
		self.scopeHeight = scope[3]-scope[1]
		self.width = self.scopeWidth-2
		self.height = self.scopeHeight-2

		self.left = self.scope[0] + 1
		self.top = self.scope[1] + 1
		self.right = self.scope[2] - 1
		self.bottom = self.scope[3] - 1
		self.centerX = self.left + self.width//2
		self.centerY = self.top + self.height//2

	def getName(self):
		return self.name

	def parseExpression(self):
		return []

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height


	def getTopLeft(self):
		return (self.left, self.top)

	def getTopRight(self):
		return (self.right, self.top)

	def getBottomLeft(self):
		return (self.left, self.bottom)

	def getBottomRight(self):
		return (self.right, self.bottom)


	def getTop(self):
		return (self.centerX, self.top)

	def getBottom(self):
		return (self.centerX, self.bottom)

	def getLeft(self):
		return (self.left, self.centerY)

	def getRight(self):
		return (self.right, self.centerY)


	def getStartPoint(self):
		return self.getTopLeft()

	def getTailPoints(self, startPoint):
		return [(False, (startPoint[0] + self.getWidth(), startPoint[1] + self.getHeight())), ]

	def getPoints(self):
		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		return pints + self.getTailPoints(points[-1][1])

	def getNewExpression(self):
		points = self.getPoints()

		point = points[0]
		isCurve = point[0]
		assert isCurve is False
		pointExpressionList = ["0000{0[0]:02X}{0[1]:02X}".format(point[1]), ]

		for point in points[1:]:
			isCurve = point[0]
			if isCurve:
				pointExpressionList.append("0002{0[0]:02X}{0[1]:02X}".format(point[1]))
			else:
				pointExpressionList.append("0001{0[0]:02X}{0[1]:02X}".format(point[1]))
		return ",".join(pointExpressionList)

	def compute_點(self, startPoint, w, h):
		assert h>0
		return [(False, (startPoint[0] + w, startPoint[1] + h))]

	def compute_圈(self, startPoint, a, b):
		assert a>0 and b>0
		CX = startPoint[0]
		CY = startPoint[1] + b

		topLeft = [CX - a, CY - b]
		top = [CX, CY - b]
		topRight = [CX + a, CY - b]
		bottomLeft = [CX - a, CY + b]
		bottom = [CX, CY + b]
		bottomRight = [CX + a, CY + b]
		left = [CX - a, CY]
		right = [CX + a, CY]

		return [
			(True, topRight), (False, right),
			(True, bottomRight), (False, bottom),
			(True, bottomLeft), (False, left),
			(True, topLeft), (False, top)
			]

	def compute_橫(self, startPoint, w):
		assert w>0
		return [(False, (startPoint[0]+w, startPoint[1])), ]

	def compute_豎(self, startPoint, h):
		assert h>0
		return [(False, (startPoint[0], startPoint[1]+h)), ]

	def compute_左(self, startPoint, w):
		assert w>0
		return [ (False, (startPoint[0]-w, startPoint[1])), ]

	def compute_上(self, startPoint, h):
		assert h>0
		return [ (False, (startPoint[0], startPoint[1]-h)), ]

	def compute_提(self, startPoint, w, h):
		assert w>0 and h>0
		return [(False, (startPoint[0]+w, startPoint[1]-h)), ]

	def compute_捺(self, startPoint, w, h):
		assert w>0 and h>0
		cPoint = [startPoint[0] + w//2, startPoint[1] + h//2]
		midPoint = (max(0, cPoint[0] - h//3), min(0xFF, cPoint[1] + w//3))
		endPoint = (startPoint[0] + width, startPoint[1] + height)
		return [(True, midPoint),
			(False, endPoint), ]

	def compute_撇(self, startPoint, w, h):
		assert (w>0 and h>0)
		return [(False, (startPoint[0] - w, startPoint[1] + h))]

	def compute_趯(self, startPoint, w, h):
		assert w>0 and h>0
		return [ (False, (startPoint[0] - w, startPoint[1] - h)), ]



	def compute_撇鉤之撇(self, startPoint, w, h):
		assert w>0 and h>0
		return [(True, (startPoint[0], startPoint[1] + h)),
			(False, (startPoint[0] - w, startPoint[1] + h)),
			]

	def compute_斜鉤之斜(self, startPoint, w, h):
		assert w>0 and h>0
		return [(True, (startPoint[0] + w//5, startPoint[1] + h*4//5)),
			(False, (startPoint[0] + w, startPoint[1] + h)),
			]

	def compute_曲(self, startPoint, cr):
		assert cr>0
		return [ (True, (startPoint[0], startPoint[1] + cr)),
			(False, (startPoint[0] + cr, startPoint[1] + cr)),]

	def compute_撇曲(self, startPoint, wl, wr, h, cr):
		assert wl>0 and wr>0 and h>0
		midPoint2 = [startPoint[0] - wl, startPoint[1] + h]

		tmp = cr

		midPoint1 = [midPoint2[0] + tmp, startPoint[1] + (wl - tmp) * h // wl]
		midPoint3 = [midPoint2[0] + tmp, startPoint[1] + h]
		midPoint4 = [startPoint[0] + wr , startPoint[1] + h]

		return [ (False, midPoint1), (True, midPoint2), (False, midPoint3), (False, midPoint4), ]


class StrokeObject_點(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[1])>0
		return [int(l[0]), int(l[1])]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w=paramList[0]
		h=paramList[1]
		if w>0:
			return self.getTopLeft()
		else:
			return self.getTopRight()

	def getPoints(self):
		paramList=self.parseExpression()
		w=paramList[0]
		h=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_點(points[-1][1], w, h))
		return points

class StrokeObject_圈(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1])]

	def getStartPoint(self):
		return self.getTop()

	def getPoints(self):
		paramList=self.parseExpression()
		a=paramList[0]
		b=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_圈(points[-1][1], a, b))
		return points

class StrokeObject_橫(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		return [int(l[0])]

	def getStartPoint(self):
		return self.getLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		return points

class StrokeObject_橫鉤(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]

		topLeft=self.getTopLeft()
		if w1>w2:
			return topLeft
		else:
			return (topLeft[0]+(w2-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		return points

class StrokeObject_橫折(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h2=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2))
		return points

class StrokeObject_橫折橫(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2))
		points.extend(self.compute_橫(points[-1][1], w3))
		return points

class StrokeObject_橫折提(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]
		h3=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2))
		points.extend(self.compute_提(points[-1][1], w3, h3))
		return points

class StrokeObject_橫折鉤(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2w3=paramList[2]
		w2=w2w3//2
		w3=w2w3//2

		topLeft = self.getTopLeft()
		if w1>(w2+w3):
			return topLeft
		else:
			return (topLeft[0]+((w2+w3)-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h2=paramList[1]
		w2w3=paramList[2]
		h3=paramList[3]
		w2=w2w3//2
		w3=w2w3//2

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇鉤之撇(points[-1][1], w2, h2))
		points.extend(self.compute_趯(points[-1][1], w3, h3))
		return points

class StrokeObject_橫折彎鉤(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h2=paramList[1]
		w2=paramList[2]
		cr=paramList[3]
		h3=paramList[4]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2 - cr))
		points.extend(self.compute_曲(points[-1][1], cr))
		points.extend(self.compute_橫(points[-1][1], w2 - cr))
		points.extend(self.compute_上(points[-1][1], h3))
		return points

class StrokeObject_橫撇(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		topLeft = self.getTopLeft()
		if w1>w2:
			return topLeft
		else:
			return (topLeft[0]+(w2-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		return points

class StrokeObject_橫撇彎鉤(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w=paramList[0]
		wb=paramList[2]

		topLeft = self.getTopLeft()
		return (topLeft[0]+(wb-w)//2, topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w=paramList[0]
		h=paramList[1]
		wb=paramList[2]
		h3=paramList[3]

		wr=(wb-w)//2
		wl=wb-wr
		cr = 0x30

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w))
		points.extend(self.compute_撇曲(points[-1][1], wr, wl, h, cr))
		points.extend(self.compute_上(points[-1][1], h3))
		return points

class StrokeObject_橫撇橫折鉤(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		assert int(l[5])>0
		assert int(l[6])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), int(l[6]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		h4=paramList[4]
		w5=paramList[5]
		h5=paramList[6]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		points.extend(self.compute_橫(points[-1][1], w3))
		points.extend(self.compute_撇鉤之撇(points[-1][1], w5//2, h4))
		points.extend(self.compute_趯(points[-1][1], w5//2, h5))
		return points

class StrokeObject_橫斜鉤(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		h3=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_斜鉤之斜(points[-1][1], w2, h2))
		points.extend(self.compute_上(points[-1][1], h3))
		return points

class StrokeObject_橫折橫折(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]
		h4=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2))
		points.extend(self.compute_橫(points[-1][1], w3))
		points.extend(self.compute_豎(points[-1][1], h4))
		return points

class StrokeObject_豎(StrokeObject):
	def parseExpression(self):
		l=self.expression[1:-1].split(',')
		assert int(l[0])>0
		return [int(l[0])]

	def getStartPoint(self):
		return self.getTop()

	def getPoints(self):
		paramList=self.parseExpression()
		h1=paramList[0]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		return points


class DCRadixParser(RadixParser):
	TAG_RADIX_SET='字根集'
	TAG_RADIX='字根'
	TAG_STROKE_GROUP='筆劃組'
	TAG_GEOMETRY='幾何'
	TAG_SCOPE='範圍'
	TAG_STROKE='筆劃'
	TAG_NAME='名稱'
	TAG_EXTRA_SCOPE='補充範圍'

	TAG_CODE_INFORMATION='編碼資訊'
	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_STROKE_EXPRESSION='筆劃資訊'

	TAG_CHARACTER_SET='字符集'
	TAG_CHARACTER='字符'

	TAG_NAME='名稱'

	def __init__(self, nameInputMethod, codeInfoEncoder):
		super().__init__(nameInputMethod, codeInfoEncoder)
		self.strokeGroupDB={}

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		strokeGroupDB={}

		strokeGroupNodeList=elementCodeInfo.findall(DCRadixParser.TAG_STROKE_GROUP)
		for strokeGroupNode in strokeGroupNodeList:
			[strokeGroupName, strokeGroup]=self.parseStrokeGroup(strokeGroupNode)
			if strokeGroupName==None:
				strokeGroupName=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT
			strokeGroupDB[strokeGroupName]=strokeGroup

		codeInfo=self.getEncoder().generateDefaultCodeInfo(strokeGroupDB)

		extraPaneDB=self.parseExtraScopeDB(elementCodeInfo)
		codeInfo.setExtraPaneDB(extraPaneDB)
		return codeInfo

	def parseRadixInfo(self, rootNode):
		radixSetNode=rootNode.find(DCRadixParser.TAG_RADIX_SET)
		if radixSetNode is not None:
			radixNodeList=radixSetNode.findall(DCRadixParser.TAG_RADIX)
			for radixNode in radixNodeList:
				radixName=radixNode.get(DCRadixParser.TAG_NAME)
				strokeGroupNodeList=radixNode.findall(DCRadixParser.TAG_STROKE_GROUP)
				for strokeGroupNode in strokeGroupNodeList:
					[strokeGroupName, strokeGroup]=self.parseStrokeGroup(strokeGroupNode)
					self.strokeGroupDB[strokeGroupName]=strokeGroup

		characterSetNode=rootNode.find(DCRadixParser.TAG_CHARACTER_SET)
		characterNodeList=characterSetNode.findall(DCRadixParser.TAG_CHARACTER)
		for characterNode in characterNodeList:
			charName=characterNode.get(DCRadixParser.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseExtraScopeDB(self, elementCodeInfo):
		extraPaneDB={}

		extraScopeNodeList=elementCodeInfo.findall(DCRadixParser.TAG_EXTRA_SCOPE)
		for extraScopeNode in extraScopeNodeList:
			paneName=extraScopeNode.attrib.get(DCRadixParser.TAG_NAME)
			pane=self.parseExtraScope(extraScopeNode)

			extraPaneDB[paneName]=pane

		return extraPaneDB

	def parseExtraScope(self, extraScopeNode):
		geometryNode=extraScopeNode.find(DCRadixParser.TAG_GEOMETRY)
		pane=self.parseGeometry(geometryNode)
		return pane

	def parseGeometry(self, geometryNode):
		descriptionRegion=geometryNode.get(DCRadixParser.TAG_SCOPE)
		pane=self.parsePane(descriptionRegion)
		return pane

	def parseStrokeGroup(self, strokeGroupNode):
		strokeGroupName=strokeGroupNode.get(DCRadixParser.TAG_NAME)

		geometryNode=strokeGroupNode.find(DCRadixParser.TAG_GEOMETRY)
		pane=self.parseGeometry(geometryNode)

		strokeGroup=self.parseStroke(pane, strokeGroupNode)
		return [strokeGroupName, strokeGroup]

	def parseStroke(self, pane, strokeGroupNode):
		strokeList=[]
		strokeNodeList=strokeGroupNode.findall(DCRadixParser.TAG_STROKE)
		for strokeNode in strokeNodeList:
			description=strokeNode.attrib.get(DCRadixParser.ATTRIB_CODE_EXPRESSION, '')

			descriptionRegion=strokeNode.get(DCRadixParser.TAG_SCOPE)
			countourPane=self.parsePane(descriptionRegion)
			if len(description)>0 and description!='XXXX':
				if description[0]=='(':
					strokeExpression=strokeNode.attrib.get(DCRadixParser.ATTRIB_STROKE_EXPRESSION, '')
					strokeObject = self.parseStrokeInfo(strokeExpression)
					if strokeObject:
						newExp = strokeObject.getNewExpression()
						strokeName = strokeObject.getName()
						actionList = self.parseStrokeActionList(newExp)
#						print(strokeObject.getName(), newExp)
					else:
						[strokeName, actionList]=self.parseStrokeNameAndAction(description)
					stroke=Stroke.fromData(pane, strokeName, actionList)

					strokeName=strokeNode.get(DCRadixParser.TAG_NAME, "瑲珩預設筆劃名")

					stroke.transform(countourPane)
					strokeList.append(stroke)
				else:
					strokeGroupName=description
					strokeGroup=self.findStrokeGroup(strokeGroupName)
					tmpStrokeGroup=strokeGroup.clone()
					tmpStrokeGroup.transform(countourPane)
					strokeList.extend(tmpStrokeGroup.getStrokeList())
		strokeGroup=StrokeGroup(pane, strokeList)
		return strokeGroup

	def parseStrokeInfo(self, strokeExpression):
		StrokeObjectMap = {
			"點": StrokeObject_點,
			"圈": StrokeObject_圈,
			"橫": StrokeObject_橫,
			"橫鉤": StrokeObject_橫鉤,
			"橫折": StrokeObject_橫折,
			"橫折橫": StrokeObject_橫折橫,
			"橫折提": StrokeObject_橫折提,
			"橫折鉤": StrokeObject_橫折鉤,
			"橫折彎鉤": StrokeObject_橫折彎鉤,
#			"橫撇": StrokeObject_橫撇,
			"橫撇彎鉤": StrokeObject_橫撇彎鉤,
			"橫撇橫折鉤": StrokeObject_橫撇橫折鉤,
			"橫斜鉤": StrokeObject_橫斜鉤,
			"橫折橫折": StrokeObject_橫折橫折,
			"豎": StrokeObject_豎,
		}

		l=strokeExpression.split(';')
		name=l[0]
		scopeDesc=l[1]

		left=int(scopeDesc[0:2], 16)
		top=int(scopeDesc[2:4], 16)
		right=int(scopeDesc[4:6], 16)
		bottom=int(scopeDesc[6:8], 16)
		scope=(left, top, right, bottom)

		strokeDesc=l[2]

		clsStrokeObject = StrokeObjectMap.get(name, None)
#		clsStrokeObject = StrokeObjectMap.get(name, StrokeObject)
		if clsStrokeObject:
			return clsStrokeObject(name, scope, strokeDesc)
		else:
			return None

	def parseStrokeActionList(self, actionDescription):
		actionList=[]
		for description in actionDescription.split(","):
			action=StrokeAction.fromDescription(description)
			actionList.append(action)
		return actionList

	def parseStrokeNameAndAction(self, strokeDescription):
		matchResult=re.match("\((.*)\)(.*)", strokeDescription)

		groups=matchResult.groups()
		strokeName=groups[0]

		strokeDescription=groups[1]

		descriptionList=strokeDescription.split(',')
		actionList=[]
		for description in descriptionList:
			action=StrokeAction.fromDescription(description)
			actionList.append(action)

		return [strokeName, actionList]

	def parsePane(self, descriptionRegion):
		left=int(descriptionRegion[0:2], 16)
		top=int(descriptionRegion[2:4], 16)
		right=int(descriptionRegion[4:6], 16)
		bottom=int(descriptionRegion[6:8], 16)
		return Pane([left, top, right, bottom])

	def findStrokeGroup(self, strokeGroupName):
		return self.strokeGroupDB.get(strokeGroupName)

