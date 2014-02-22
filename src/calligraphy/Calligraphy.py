import re
import sys

from . import quadratic
import math

class StrokeInfo:
	def __init__(self, name, scope, parameterList):
		self.name = name
		self.scope = scope
		self.parameterList=parameterList

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

	@classmethod
	def parseExpression(cls, parameterExpressionList):
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

	@staticmethod
	def computeExtreme(points, extreme, solveExtreme, retrieveValue):
		firstPointPair = points[0]
		prevPoint = firstPointPair[1]
		midPoint = None

		extremeValue = retrieveValue(prevPoint)
		for p in points[1:]:
			isCurve = p[0]
			currPoint = p[1]

			extremeValue = extreme(extremeValue, retrieveValue(currPoint))
			if isCurve:
				midPoint=currPoint
			else:
				if midPoint:
					s0, s1, s2 = retrieveValue(prevPoint), retrieveValue(midPoint), retrieveValue(currPoint)
					tmpExtremeValue = solveExtreme(s0, s1, s2)
					extremeValue = extreme(extremeValue, tmpExtremeValue)

				prevPoint=currPoint
				midPoint=None

		return extremeValue

	def computeLeft(self):
		return StrokeInfo.computeExtreme(self.getPoints(), min, quadratic.solveMin, lambda p: p[0])

	def computeRight(self):
		return StrokeInfo.computeExtreme(self.getPoints(), max, quadratic.solveMax, lambda p: p[0])

	def computeTop(self):
		return StrokeInfo.computeExtreme(self.getPoints(), min, quadratic.solveMin, lambda p: p[1])

	def computeBottom(self):
		return StrokeInfo.computeExtreme(self.getPoints(), max, quadratic.solveMax, lambda p: p[1])

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
#		assert w>0
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
		endPoint = (startPoint[0] + w, startPoint[1] + h)
		return [(True, midPoint),
			(False, endPoint), ]

	def compute_撇(self, startPoint, w, h):
		assert (w>0 and h>0)
		return [(False, (startPoint[0] - w, startPoint[1] + h))]

	def compute_鉤(self, startPoint, w, h):
		assert w>0 and h>0
		return [ (False, (startPoint[0] - w, startPoint[1] - h)), ]

	def compute_臥捺(self, startPoint, w, h):
		assert w>0 and h>0
		halfW = w//2
		halfH = h//2

		endPoint = [startPoint[0] + w, startPoint[1] + h]
		cPoint = [startPoint[0] + halfW, startPoint[1] + halfH]
		midPoint1 = [startPoint[0]+halfW//2+halfH//4, startPoint[1]+halfH//2-halfW//4]
		midPoint2 = [cPoint[0]+halfW//2-halfH//4, min(0xFF, cPoint[1]+halfH//2+halfW//4)]
		return [(True, midPoint1),
			(False, cPoint),
			(True, midPoint2),
			(False, endPoint),]


	def compute_豎撇(self, startPoint, w, hs, hp):
		assert w>0 and hs>0 and hp>0

		startPoint = self.getStartPoint()
		midPoint1 = [startPoint[0], startPoint[1] + hs]
		midPoint2 = [midPoint1[0], midPoint1[1] + hp]
		endPoint = [midPoint2[0] - w, midPoint2[1]]

		return [ (False, midPoint1), (True, midPoint2), (False, endPoint) ]


	def compute_彎鉤之彎(self, startPoint, w1, h1):
		assert h1>0
		cPoint = [startPoint[0] + w1//2, startPoint[1] + h1//2]
		midPoint1 = [min(0xFF, cPoint[0] + h1//2), max(0, cPoint[1] - w1//2)]
		midPoint2 = [startPoint[0] + w1, startPoint[1] + h1]
		return [(True, midPoint1),
			(False, midPoint2),
			]

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


class StrokeInfo_點(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[1])>0
		return [int(l[0]), int(l[1])]

	def getStartPoint(self):
		paramList=self.parameterList
		w=paramList[0]
		h=paramList[1]
		if w>0:
			return self.getTopLeft()
		else:
			return self.getTopRight()

	def getPoints(self):
		paramList=self.parameterList
		w=paramList[0]
		h=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_點(points[-1][1], w, h))
		return points

class StrokeInfo_圈(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1])]

	def getStartPoint(self):
		return self.getTop()

	def getPoints(self):
		paramList=self.parameterList
		a=paramList[0]
		b=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_圈(points[-1][1], a, b))
		return points

class StrokeInfo_橫(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==1
		assert int(l[0])>0
		return [int(l[0])]

	def getStartPoint(self):
		return self.getLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		return points

class StrokeInfo_橫鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]

		topLeft=self.getTopLeft()
		return (topLeft[0]+max(0, w2-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		return points

class StrokeInfo_橫折(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2))
		return points

class StrokeInfo_橫折折(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2))
		points.extend(self.compute_橫(points[-1][1], w3))
		return points

class StrokeInfo_橫折提(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
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

class StrokeInfo_橫折鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==5
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		w3=paramList[3]

		topLeft = self.getTopLeft()
		return (topLeft[0]+max(0, (w2+w3)-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇鉤之撇(points[-1][1], w2, h2))
		points.extend(self.compute_鉤(points[-1][1], w3, h3))
		return points

class StrokeInfo_橫折彎(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w2=paramList[2]
		cr=paramList[3]
#		h3=paramList[4]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2 - cr))
		points.extend(self.compute_曲(points[-1][1], cr))
		points.extend(self.compute_橫(points[-1][1], w2 - cr))
#		points.extend(self.compute_上(points[-1][1], h3))
		return points

class StrokeInfo_橫撇(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		topLeft = self.getTopLeft()
		return (topLeft[0]+max(0, w2-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		return points

class StrokeInfo_橫斜彎鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==6
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		assert int(l[5])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2l=paramList[2]
		w2r=paramList[3]

		topLeft = self.getTopLeft()
		return (topLeft[0]+(w2l-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w2l=paramList[2]
		w2r=paramList[3]
		cr=paramList[4]
		h3=paramList[5]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇曲(points[-1][1], w2l, w2r, h2, cr))
		points.extend(self.compute_上(points[-1][1], h3))
		return points

class StrokeInfo_橫折折折鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==8
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		assert int(l[5])>0
		assert int(l[6])>0
		assert int(l[7])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), int(l[6]), int(l[7]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		w4=paramList[4]
		h4=paramList[5]
		w5=paramList[6]
		h5=paramList[7]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		points.extend(self.compute_橫(points[-1][1], w3))
		points.extend(self.compute_撇鉤之撇(points[-1][1], w4, h4))
		points.extend(self.compute_鉤(points[-1][1], w5, h5))
		return points

class StrokeInfo_橫斜鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
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

class StrokeInfo_橫折折折(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert len(l)==4
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
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

class StrokeInfo_豎(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==1
		assert int(l[0])>0
		return [int(l[0]), ]

	def getStartPoint(self):
		return self.getTop()

	def getPoints(self):
		paramList=self.parameterList
		h1=paramList[0]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		return points

class StrokeInfo_豎折(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_橫(points[-1][1], w2))
		return points

class StrokeInfo_豎提(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_提(points[-1][1], w2, h2))
		return points

class StrokeInfo_豎折折(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h3=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_橫(points[-1][1], w2))
		points.extend(self.compute_豎(points[-1][1], h3))
		return points

class StrokeInfo_豎折彎鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==7
		assert int(l[0])>=0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		assert int(l[5])>0
		assert int(l[6])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), int(l[6]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0] + w1, topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]
		w4=paramList[5]
		h4=paramList[6]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		if w1>0:
			points.extend(self.compute_撇(points[-1][1], w1, h1))
		elif w1<0:
			assert False
		else:
			points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_橫(points[-1][1], w2))
		points.extend(self.compute_撇鉤之撇(points[-1][1], w3, h3))
		points.extend(self.compute_鉤(points[-1][1], w4, h4))
		return points

class StrokeInfo_豎彎鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		h1=paramList[0]
		w1=paramList[1]
		cr=paramList[2]
		h2=paramList[3]

		topLeft = self.getTopLeft()
		return (topLeft[0], topLeft[1]+max(0, h2-h1))

	def getPoints(self):
		paramList=self.parameterList
		h1=paramList[0]
		w1=paramList[1]
		cr=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1-cr))
		points.extend(self.compute_曲(points[-1][1], cr))
		points.extend(self.compute_橫(points[-1][1], w1-cr))
		points.extend(self.compute_上(points[-1][1], h2))
		return points

class StrokeInfo_豎彎(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		cr=paramList[0]
		w=paramList[1]
		h=paramList[2]

		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		cr=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_曲(points[-1][1], cr))
		points.extend(self.compute_橫(points[-1][1], w1))
		return points

class StrokeInfo_豎鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopRight()

	def getPoints(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		hs = h1 - h2*3
		hp = h2*3
		wp = w2//4

		wg=w2//2
		hg=wg

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎撇(points[-1][1], wp, hs, hp))
		points.extend(self.compute_鉤(points[-1][1], wg, hg))
		return points

class StrokeInfo_斜鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_斜鉤之斜(points[-1][1], w1, h1))
		points.extend(self.compute_上(points[-1][1], h2))
		return points

class StrokeInfo_彎鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
#		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		topLeft=self.getTopLeft()
		return (topLeft[0]+max(0,w2-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_彎鉤之彎(points[-1][1], w1, h1))
		points.extend(self.compute_鉤(points[-1][1], w2, h2))
		return points

class StrokeInfo_撇鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
#		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		topLeft=self.getTopLeft()
		return (topLeft[0]-w1+w2, topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_彎鉤之彎(points[-1][1], w1, h1))
		points.extend(self.compute_鉤(points[-1][1], w2, h2))
		return points

class StrokeInfo_撇(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopRight()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_撇(points[-1][1], w1, h1))
		return points

class StrokeInfo_撇點(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0]+w1, topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_撇(points[-1][1], w1, h1))
		points.extend(self.compute_點(points[-1][1], w2, h2))
		return points

class StrokeInfo_撇橫(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
#		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0]+w1, topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_撇(points[-1][1], w1, h1))
		if h2>0:
			points.extend(self.compute_點(points[-1][1], w2, h2))
		elif h2<0:
			points.extend(self.compute_提(points[-1][1], w2, -h2))
		else:
			points.extend(self.compute_橫(points[-1][1], w2))
		return points

class StrokeInfo_撇橫撇(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==5
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[2]
		w3=paramList[3]

		paramList=self.parameterList
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0]+w1+max(0, w3-w2), topLeft[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_撇(points[-1][1], w1, h1))
		points.extend(self.compute_橫(points[-1][1], w2))
		points.extend(self.compute_撇(points[-1][1], w3, h3))
		return points

class StrokeInfo_豎撇(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopRight()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

		hs = h1 - h1//2
		hp = h1 - (hs)
		wp = w1

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎撇(points[-1][1], w1, hs, hp))
		return points

class StrokeInfo_提(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getBottomLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_提(points[-1][1], w1, h1))
		return points

class StrokeInfo_捺(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

		topRight = self.getTopRight()
		return (topRight[0]-w1, topRight[1])

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_捺(points[-1][1], w1, h1))
		return points

class StrokeInfo_臥捺(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		h1=paramList[1]

		left = self.getLeft()
		return (left[0], left[1]-h1//2)

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_臥捺(points[-1][1], w1, h1))
		return points

class StrokeInfo_提捺(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parameterList
		h1=paramList[1]

		topLeft = self.getTopLeft()
		return (topLeft[0], topLeft[1]+h1)

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_提(points[-1][1], w1, h1))
		points.extend(self.compute_捺(points[-1][1], w2, h2))
		return points

class StrokeInfo_橫捺(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_捺(points[-1][1], w2, h2))
		return points

StrokeInfoMap = {
	"點": StrokeInfo_點,
#	"長頓點": StrokeInfo_點,
	"圈": StrokeInfo_圈,
	"橫": StrokeInfo_橫,
	"橫鉤": StrokeInfo_橫鉤,
	"橫折": StrokeInfo_橫折,
	"橫折折": StrokeInfo_橫折折,
	"橫折提": StrokeInfo_橫折提,
	"橫折鉤": StrokeInfo_橫折鉤,
	"橫折彎": StrokeInfo_橫折彎,
	"橫撇": StrokeInfo_橫撇,
	"橫斜彎鉤": StrokeInfo_橫斜彎鉤,
	"橫折折折鉤": StrokeInfo_橫折折折鉤,
	"橫斜鉤": StrokeInfo_橫斜鉤,
	"橫折折折": StrokeInfo_橫折折折,
	"豎": StrokeInfo_豎,
	"豎折": StrokeInfo_豎折,
	"豎提": StrokeInfo_豎提,
	"豎折折": StrokeInfo_豎折折,
	"豎折彎鉤": StrokeInfo_豎折彎鉤,
	"豎彎鉤": StrokeInfo_豎彎鉤,
	"豎彎": StrokeInfo_豎彎,
	"豎鉤": StrokeInfo_豎鉤,
	"扁斜鉤": StrokeInfo_豎彎鉤,
	"斜鉤": StrokeInfo_斜鉤,
	"彎鉤": StrokeInfo_彎鉤,
	"撇鉤": StrokeInfo_撇鉤,

	"撇": StrokeInfo_撇,
	"撇點": StrokeInfo_撇點,
	"撇橫": StrokeInfo_撇橫,
	"撇提": StrokeInfo_撇橫,
	"撇折": StrokeInfo_撇橫,
	"撇橫撇": StrokeInfo_撇橫撇,
	"豎撇": StrokeInfo_豎撇,
	"提": StrokeInfo_提,
	"捺": StrokeInfo_捺,
	"臥捺": StrokeInfo_臥捺,
	"提捺": StrokeInfo_提捺,
	"橫捺": StrokeInfo_橫捺,
}


class Pane:
	WIDTH=0x100
	HEIGHT=0x100
	X_MAX=0xFF
	Y_MAX=0xFF

	DEFAULT_REGION=[0, 0, X_MAX, Y_MAX]

	def __init__(self, region=DEFAULT_REGION):
		[left, top, right, bottom]=region
		self.left=left
		self.top=top
		self.right=right
		self.bottom=bottom

		self.name="預設範圍"

		self.setup()

	def clone(self):
		return Pane(self.getAsList())

	def setup(self):
		self.hScale=self.width*1./Pane.WIDTH
		self.vScale=self.height*1./Pane.HEIGHT

	@property
	def width(self):
		return self.right-self.left+1

	@property
	def height(self):
		return self.bottom-self.top+1

	def setName(self, name):
		self.name=name

	def getName(self):
		return self.name

	def getAsList(self):
		return [self.left, self.top, self.right, self.bottom]

	def getLeft(self):
		return self.left

	def getTop(self):
		return self.top

	def getRight(self):
		return self.right

	def getBottom(self):
		return self.bottom

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getHScale(self):
		return self.hScale

	def getVScale(self):
		return self.vScale

	def transformPoint(self, point):
		[x, y]=point
		left=self.getLeft()
		top=self.getTop()

		hScale=self.getHScale()
		vScale=self.getVScale()

		newX=int(x*hScale)+left
		newY=int(y*vScale)+top

		return (newX, newY)

	def transformPane(self, pane):
		(left, top)=self.transformPoint((pane.left, pane.top))
		(right, bottom)=self.transformPoint((pane.right, pane.bottom))

		pane.left=left
		pane.top=top
		pane.right=right
		pane.bottom=bottom

		pane.setup()

Pane.DEFAULT_PANE=Pane()


class Writing:
	def __init__(self, contourPane):
		self.boundaryPane=Pane.DEFAULT_PANE
		self.contourPane=contourPane

	def getBoundaryPane(self):
		return self.boundaryPane

	def getContourPane(self):
		return self.contourPane

	# 多型
	def transform(self, pane):
		pass

class StrokeState:
	def __init__(self, targetPane=Pane()):
		self.targetPane=targetPane

	def clone(self):
		return StrokeState(self.targetPane.clone())

	def getTargetPane(self):
		return self.targetPane

class Stroke(Writing):
	def __init__(self, strokeInfo, state=StrokeState()):
		super().__init__(Pane())
		self.strokeInfo=strokeInfo
		self.state=state

	def clone(self):
		return Stroke(self.strokeInfo, self.state.clone())

	def getTypeName(self):
		return self.strokeInfo.getTypeName()

	def getState(self):
		return self.state

	def getStrokeInfo(self):
		return self.strokeInfo

	# 多型
	def transform(self, pane):
		pane.transformPane(self.state.getTargetPane())

	def computeLeft(self):
		return self.strokeInfo.computeLeft()

	def computeRight(self):
		return self.strokeInfo.computeRight()

	def computeTop(self):
		return self.strokeInfo.computeTop()

	def computeBottom(self):
		return self.strokeInfo.computeBottom()

class StrokeGroup(Writing):
	def __init__(self, contourPane, strokeList):
		super().__init__(contourPane)

		self.strokeList=strokeList

	def clone(self):
		strokeList=[s.clone() for s in self.strokeList]
		return StrokeGroup(self.contourPane, strokeList)

	def getStrokeList(self):
		return self.strokeList

	def getCount(self):
		return len(self.strokeList)

	# 多型
	def transform(self, pane):
		for stroke in self.strokeList:
			stroke.transform(pane)

	def computeLeft(self):
		return min([s.strokeInfo.computeLeft() for s in self.strokeList])

	def computeRight(self):
		return max([s.strokeInfo.computeRight() for s in self.strokeList])

	def computeTop(self):
		return min([s.strokeInfo.computeTop() for s in self.strokeList])

	def computeBottom(self):
		return max([s.strokeInfo.computeBottom() for s in self.strokeList])

