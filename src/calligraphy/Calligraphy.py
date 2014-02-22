import re
import sys

from . import quadratic
import math

class StrokeDrawing:
	def __init__(self, points):
		self.points = points

	def computeLeft(self):
		return StrokeInfo.computeExtreme(self.points, min, quadratic.solveMin, lambda p: p[0])

	def computeRight(self):
		return StrokeInfo.computeExtreme(self.points, max, quadratic.solveMax, lambda p: p[0])

	def computeTop(self):
		return StrokeInfo.computeExtreme(self.points, min, quadratic.solveMin, lambda p: p[1])

	def computeBottom(self):
		return StrokeInfo.computeExtreme(self.points, max, quadratic.solveMax, lambda p: p[1])

	def computeScope(self):
		return (
			self.computeLeft(), self.computeTop(),
			self.computeRight(), self.computeBottom(),
			)

class StrokeInfo:
	def __init__(self, parameterList):
		self.parameterList=parameterList

	def isValid(self):
		return false

	@classmethod
	def parseExpression(cls, parameterExpressionList):
		return []

	def computePoints(self):
		points=[(False, startPoint), (False, startPoint), ]
		return points

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
		scale = max(3, w/h*2, h/w*2)
		midPoint = (cPoint[0] - h//scale, cPoint[1] + w//scale)
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
		midPoint2 = [cPoint[0]+halfW//2-halfH//4, cPoint[1]+halfH//2+halfW//4]
		return [(True, midPoint1),
			(False, cPoint),
			(True, midPoint2),
			(False, endPoint),]


	def compute_豎撇(self, startPoint, w, hs, hp):
		assert w>0 and hs>0 and hp>0

		midPoint1 = [startPoint[0], startPoint[1] + hs]
		midPoint2 = [midPoint1[0], midPoint1[1] + hp]
		endPoint = [midPoint2[0] - w, midPoint2[1]]

		return [ (False, midPoint1), (True, midPoint2), (False, endPoint) ]


	def compute_彎鉤之彎(self, startPoint, w1, h1):
		assert h1>0
		cPoint = [startPoint[0] + w1//2, startPoint[1] + h1//2]
		midPoint1 = [cPoint[0] + h1//2, cPoint[1] - w1//2]
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

	def isValid(self):
		paramList=self.parameterList
		w=paramList[0]
		h=paramList[1]
		return h>0
#		return w>0 and h>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w=paramList[0]
		h=paramList[1]

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

	def isValid(self):
		paramList=self.parameterList
		a=paramList[0]
		b=paramList[1]
		return a>0 and b>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		a=paramList[0]
		b=paramList[1]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		return w1>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		return w1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		return w1>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]
		return w1>0 and h2>0 and w3>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]
		h3=paramList[3]
		return w1>0 and h2>0 and w3>0 and h3>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]
		h3=paramList[3]

		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2))
		points.extend(self.compute_提(points[-1][1], w3, h3))
		return points

class StrokeInfo_橫折折撇(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		assert int(l[5])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), ]

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		w4=paramList[4]
		h4=paramList[5]
		return w1>0 and w2>0 and h2>0 and w3>0 and w4>0 and h4>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		w4=paramList[4]
		h4=paramList[5]

		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		points.extend(self.compute_橫(points[-1][1], w3))
		points.extend(self.compute_撇(points[-1][1], w4, h4))
		return points

class StrokeInfo_橫撇彎鉤(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		assert int(l[5])>0
		assert int(l[6])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), int(l[6]), ]

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]
		w4=paramList[5]
		h4=paramList[6]
		return w1>0 and w2>0 and h2>0 and w3>0 and h3>0 and w4>0 and h4>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]
		w4=paramList[5]
		h4=paramList[6]

		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_撇(points[-1][1], w2, h2))
		points.extend(self.compute_彎鉤之彎(points[-1][1], w3, h3))
		points.extend(self.compute_鉤(points[-1][1], w4, h4))
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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]
		return w1>0 and w2>0 and h2>0 and w3>0 and h3>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w2=paramList[2]
		cr=paramList[3]
		return w1>0 and h2>0 and w2>0 and cr>0 and(h2-cr)>0 and (w2-cr)>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w2=paramList[2]
		cr=paramList[3]

		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_豎(points[-1][1], h2 - cr))
		points.extend(self.compute_曲(points[-1][1], cr))
		points.extend(self.compute_橫(points[-1][1], w2 - cr))
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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		return w1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w2l=paramList[2]
		w2r=paramList[3]
		cr=paramList[4]
		h3=paramList[5]
		return w1>0 and h2>0 and w2l>0 and w2r>0 and cr>0 and h3>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w2l=paramList[2]
		w2r=paramList[3]
		cr=paramList[4]
		h3=paramList[5]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		w4=paramList[4]
		h4=paramList[5]
		w5=paramList[6]
		h5=paramList[7]
		return w1>0 and w2>0 and h2>0 and w3>0 and w4>0 and h4>0 and w5>0 and h5>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		w3=paramList[3]
		w4=paramList[4]
		h4=paramList[5]
		w5=paramList[6]
		h5=paramList[7]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		h3=paramList[3]
		return w1>0 and w2>0 and h2>0 and h3>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		h3=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]
		h4=paramList[3]
		return w1>0 and h2>0 and w3>0 and h4>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h2=paramList[1]
		w3=paramList[2]
		h4=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		h1=paramList[0]
		return h1>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		h1=paramList[0]

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

	def isValid(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		return h1>0 and w2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]

		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_橫(points[-1][1], w2))
		return points

class StrokeInfo_豎彎左(StrokeInfo):
	@classmethod
	def parseExpression(cls, parameterExpressionList):
		l=parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def isValid(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		return h1>0 and w2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]

		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_左(points[-1][1], w2))
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

	def isValid(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		return h1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

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

	def isValid(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h3=paramList[2]
		return h1>0 and w2>0 and h3>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h3=paramList[2]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]
		w4=paramList[5]
		h4=paramList[6]
		return w1>=0 and h1>0 and w2>0 and w3>0 and h3>0 and w4>0 and h4>0
#		return w1>0 and h1>0 and w2>0 and w3>0 and h3>0 and w4>0 and h4>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]
		w4=paramList[5]
		h4=paramList[6]

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

	def isValid(self):
		paramList=self.parameterList
		h1=paramList[0]
		w1=paramList[1]
		cr=paramList[2]
		h2=paramList[3]
		return h1>0 and w1>0 and cr>0 and h2>0 and(h1-cr)>0 and (w1-cr)>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		h1=paramList[0]
		w1=paramList[1]
		cr=paramList[2]
		h2=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		cr=paramList[2]
		return w1>0 and h1>0 and cr>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		cr=paramList[2]

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

	def isValid(self):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		return h1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		h1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		hs = h1 - h2*3
		hp = h2*3
		wp = w2//4

		wg=w2//2
		hg=wg

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		h2=paramList[2]
		return w1>0 and h1>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		h2=paramList[2]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]
		return h1>0 and w2>0 and h2>0
#		return w1>0 and h1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]
		return h1>0 and w2>0 and h2>0
#		return w1>0 and h1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		return w1>0 and h1>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]
		return w1>0 and h1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]
		return w1>0 and h1>0 and w2>0
#		return w1>0 and h1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]
		return w1>0 and h1>0 and w2>0 and w3>0 and h3>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		w3=paramList[3]
		h3=paramList[4]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		return w1>0 and h1>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

		hs = h1 - h1//2
		hp = h1 - (hs)
		wp = w1

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		return w1>0 and h1>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		return w1>0 and h1>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		return w1>0 and h1>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]
		return w1>0 and h1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

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

	def isValid(self):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]
		return w1>0 and w2>0 and h2>0

	def computePoints(self, startPoint):
		paramList=self.parameterList
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

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
	"橫折折撇": StrokeInfo_橫折折撇,
	"橫撇彎鉤": StrokeInfo_橫撇彎鉤,
	"橫折鉤": StrokeInfo_橫折鉤,
	"橫折彎": StrokeInfo_橫折彎,
	"橫撇": StrokeInfo_橫撇,
	"橫斜彎鉤": StrokeInfo_橫斜彎鉤,
	"橫折折折鉤": StrokeInfo_橫折折折鉤,
	"橫斜鉤": StrokeInfo_橫斜鉤,
	"橫折折折": StrokeInfo_橫折折折,
	"豎": StrokeInfo_豎,
	"豎折": StrokeInfo_豎折,
	"豎彎左": StrokeInfo_豎彎左,
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
	def __init__(self, startPoint, strokeInfo, state=StrokeState()):
		super().__init__(Pane())

		self.startPoint=startPoint
		self.strokeInfo=strokeInfo
		self.state=state

	def clone(self):
		return Stroke(self.startPoint, self.strokeInfo, self.state.clone())

	def getState(self):
		return self.state

	def getStrokeInfo(self):
		return self.strokeInfo

	def isValid(self):
		return self.strokeInfo.isValid()

	# 多型
	def transform(self, pane):
		pane.transformPane(self.state.getTargetPane())

	def getPoints(self):
		def toValid(point):
			x, y = point
			newX = max(0, min(0xFF, x))
			newY = max(0, min(0xFF, y))
			return (newX, newY)

		strokeState=self.getState()
		pane=strokeState.getTargetPane()

		startPoint=self.startPoint
		points=self.strokeInfo.computePoints(startPoint)
		newPoints = [(isCurve, pane.transformPoint(point)) for (isCurve, point) in points]
		return newPoints

	def computeScope(self):
		return StrokeDrawing(self.getPoints()).computeScope()

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

	def isValid(self):
		return all([stroke.isValid() for stroke in self.strokeList])

	# 多型
	def transform(self, pane):
		for stroke in self.strokeList:
			stroke.transform(pane)

	def computeScope(self):
		scopes=[s.computeScope() for s in self.strokeList]
		left=min(list(zip(*scopes))[0])
		top=min(list(zip(*scopes))[1])
		right=min(list(zip(*scopes))[2])
		bottom=min(list(zip(*scopes))[3])
		return (left, top, right, bottom)

