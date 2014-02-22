import re
import sys

class StrokeObject:
	def __init__(self, name, scope, parameterExpressionList):
		self.name = name
		self.scope = scope
		self.parameterExpressionList = parameterExpressionList
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


class StrokeObject_點(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==2
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
		l=self.parameterExpressionList
		assert len(l)==2
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
		l=self.parameterExpressionList
		assert len(l)==1
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
		l=self.parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]

		topLeft=self.getTopLeft()
		return (topLeft[0]+max(0, w2-w1), topLeft[1])

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
		l=self.parameterExpressionList
		assert len(l)==2
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

class StrokeObject_橫折折(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
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
		l=self.parameterExpressionList
		assert len(l)==4
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
		l=self.parameterExpressionList
		assert len(l)==5
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]
		w3=paramList[3]

		topLeft = self.getTopLeft()
		return (topLeft[0]+max(0, (w2+w3)-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
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

class StrokeObject_橫折彎(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
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

class StrokeObject_橫撇(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
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
		return (topLeft[0]+max(0, w2-w1), topLeft[1])

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

class StrokeObject_橫斜彎鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==6
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		assert int(l[5])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2l=paramList[2]
		w2r=paramList[3]

		topLeft = self.getTopLeft()
		return (topLeft[0]+(w2l-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
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

class StrokeObject_橫折折折鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
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
		paramList=self.parseExpression()
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

class StrokeObject_橫斜鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
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

class StrokeObject_橫折折折(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert len(l)==4
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
		l=self.parameterExpressionList
		assert len(l)==1
		assert int(l[0])>0
		return [int(l[0]), ]

	def getStartPoint(self):
		return self.getTop()

	def getPoints(self):
		paramList=self.parseExpression()
		h1=paramList[0]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		return points

class StrokeObject_豎折(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		h1=paramList[0]
		w2=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_橫(points[-1][1], w2))
		return points

class StrokeObject_豎提(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		h1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_提(points[-1][1], w2, h2))
		return points

class StrokeObject_豎折折(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		h1=paramList[0]
		w2=paramList[1]
		h3=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_橫(points[-1][1], w2))
		points.extend(self.compute_豎(points[-1][1], h3))
		return points

class StrokeObject_豎折彎鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
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
		paramList=self.parseExpression()
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0] + w1, topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
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

class StrokeObject_豎彎鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		h1=paramList[0]
		w1=paramList[1]
		cr=paramList[2]
		h2=paramList[3]

		topLeft = self.getTopLeft()
		return (topLeft[0], topLeft[1]+max(0, h2-h1))

	def getPoints(self):
		paramList=self.parseExpression()
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

class StrokeObject_豎彎(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		cr=paramList[0]
		w=paramList[1]
		h=paramList[2]

		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		cr=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎(points[-1][1], h1))
		points.extend(self.compute_曲(points[-1][1], cr))
		points.extend(self.compute_橫(points[-1][1], w1))
		return points

class StrokeObject_豎鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopRight()

	def getPoints(self):
		paramList=self.parseExpression()
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

class StrokeObject_斜鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_斜鉤之斜(points[-1][1], w1, h1))
		points.extend(self.compute_上(points[-1][1], h2))
		return points

class StrokeObject_彎鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
#		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		topLeft=self.getTopLeft()
		return (topLeft[0]+max(0,w2-w1), topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_彎鉤之彎(points[-1][1], w1, h1))
		points.extend(self.compute_鉤(points[-1][1], w2, h2))
		return points

class StrokeObject_撇鉤(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
#		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		topLeft=self.getTopLeft()
		return (topLeft[0]-w1+w2, topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_彎鉤之彎(points[-1][1], w1, h1))
		points.extend(self.compute_鉤(points[-1][1], w2, h2))
		return points

class StrokeObject_撇(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopRight()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_撇(points[-1][1], w1, h1))
		return points

class StrokeObject_撇點(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0]+w1, topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_撇(points[-1][1], w1, h1))
		points.extend(self.compute_點(points[-1][1], w2, h2))
		return points

class StrokeObject_撇橫(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
#		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0]+w1, topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
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

class StrokeObject_撇橫撇(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==5
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		assert int(l[4])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[2]
		w3=paramList[3]

		paramList=self.parseExpression()
		w1=paramList[0]

		topLeft = self.getTopLeft()
		return (topLeft[0]+w1+max(0, w3-w2), topLeft[1])

	def getPoints(self):
		paramList=self.parseExpression()
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

class StrokeObject_豎撇(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getTopRight()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]

		hs = h1 - h1//2
		hp = h1 - (hs)
		wp = w1

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_豎撇(points[-1][1], w1, hs, hp))
		return points

class StrokeObject_提(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		return self.getBottomLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_提(points[-1][1], w1, h1))
		return points

class StrokeObject_捺(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]

		topRight = self.getTopRight()
		return (topRight[0]-w1, topRight[1])

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_捺(points[-1][1], w1, h1))
		return points

class StrokeObject_臥捺(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==2
		assert int(l[0])>0
		assert int(l[1])>0
		return [int(l[0]), int(l[1]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		h1=paramList[1]

		left = self.getLeft()
		return (left[0], left[1]-h1//2)

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_臥捺(points[-1][1], w1, h1))
		return points

class StrokeObject_提捺(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==4
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		assert int(l[3])>0
		return [int(l[0]), int(l[1]), int(l[2]), int(l[3]), ]

	def getStartPoint(self):
		paramList=self.parseExpression()
		h1=paramList[1]

		topLeft = self.getTopLeft()
		return (topLeft[0], topLeft[1]+h1)

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		h1=paramList[1]
		w2=paramList[2]
		h2=paramList[3]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_提(points[-1][1], w1, h1))
		points.extend(self.compute_捺(points[-1][1], w2, h2))
		return points

class StrokeObject_橫捺(StrokeObject):
	def parseExpression(self):
		l=self.parameterExpressionList
		assert len(l)==3
		assert int(l[0])>0
		assert int(l[1])>0
		assert int(l[2])>0
		return [int(l[0]), int(l[1]), int(l[2]), ]

	def getStartPoint(self):
		return self.getTopLeft()

	def getPoints(self):
		paramList=self.parseExpression()
		w1=paramList[0]
		w2=paramList[1]
		h2=paramList[2]

		startPoint = self.getStartPoint()
		points=[(False, startPoint), ]
		points.extend(self.compute_橫(points[-1][1], w1))
		points.extend(self.compute_捺(points[-1][1], w2, h2))
		return points

StrokeObjectMap = {
	"點": StrokeObject_點,
#	"長頓點": StrokeObject_點,
	"圈": StrokeObject_圈,
	"橫": StrokeObject_橫,
	"橫鉤": StrokeObject_橫鉤,
	"橫折": StrokeObject_橫折,
	"橫折折": StrokeObject_橫折折,
	"橫折提": StrokeObject_橫折提,
	"橫折鉤": StrokeObject_橫折鉤,
	"橫折彎": StrokeObject_橫折彎,
	"橫撇": StrokeObject_橫撇,
	"橫斜彎鉤": StrokeObject_橫斜彎鉤,
	"橫折折折鉤": StrokeObject_橫折折折鉤,
	"橫斜鉤": StrokeObject_橫斜鉤,
	"橫折折折": StrokeObject_橫折折折,
	"豎": StrokeObject_豎,
	"豎折": StrokeObject_豎折,
	"豎提": StrokeObject_豎提,
	"豎折折": StrokeObject_豎折折,
	"豎折彎鉤": StrokeObject_豎折彎鉤,
	"豎彎鉤": StrokeObject_豎彎鉤,
	"豎彎": StrokeObject_豎彎,
	"豎鉤": StrokeObject_豎鉤,
	"扁斜鉤": StrokeObject_豎彎鉤,
	"斜鉤": StrokeObject_斜鉤,
	"彎鉤": StrokeObject_彎鉤,
	"撇鉤": StrokeObject_撇鉤,

	"撇": StrokeObject_撇,
	"撇點": StrokeObject_撇點,
	"撇橫": StrokeObject_撇橫,
	"撇提": StrokeObject_撇橫,
	"撇折": StrokeObject_撇橫,
	"撇橫撇": StrokeObject_撇橫撇,
	"豎撇": StrokeObject_豎撇,
	"提": StrokeObject_提,
	"捺": StrokeObject_捺,
	"臥捺": StrokeObject_臥捺,
	"提捺": StrokeObject_提捺,
	"橫捺": StrokeObject_橫捺,
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


class StrokeAction:
	ACTION_START="0000"
	ACTION_END="0001"
	ACTION_CURVE="0002"

	ActionStrToNumDict={
		ACTION_START : 0,
		ACTION_END : 1,
		ACTION_CURVE : 2,
	}

	ActionNumToStrDict={
		0: ACTION_START,
		1: ACTION_END,
		2: ACTION_CURVE,
	}

	def __init__(self, action, point):
		self.action=action
		self.point=point

	@staticmethod
	def fromDescription(description):
		actionStr=description[0:4]
		action=StrokeAction.ActionStrToNumDict[actionStr]
		x=int(description[4:6], 16)
		y=int(description[6:8], 16)
		point=(x, y)
		return StrokeAction(action, point)

	def getCode(self, pane):
		(x, y)=pane.transformPoint(self.point)
		code="%02X%02X"%(x, y)
		return StrokeAction.ActionNumToStrDict[self.action]+code

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

class StrokeInfo(Writing):
	DEFAULT_INSTANCE_NAME='瑲珩預設筆劃名'

	def __init__(self, contourPane, strokeName, actionList):
		super().__init__(contourPane)

		assert (strokeName in StrokeObjectMap), "不認得的筆畫名稱: %s"%strokeName

		self.typeName=strokeName

		self.actionList=actionList

	def getTypeName(self):
		return self.typeName

	def getCodeList(self, pane):
		codeList=[action.getCode(pane) for action in self.actionList]
		return codeList

class StrokeState:
	def __init__(self, targetPane=Pane()):
		self.targetPane=targetPane

	def clone(self):
		return StrokeState(self.targetPane.clone())

	def getTargetPane(self):
		return self.targetPane

class Stroke(Writing):
	def __init__(self, strokeInfo, state):
		super().__init__(strokeInfo.contourPane)
		self.strokeInfo=strokeInfo
		self.state=state

	@staticmethod
	def fromStrokeExpression(contourPane, strokeExpression):
		strokeObject = Stroke.parseStrokeInfo(strokeExpression)

		def parseStrokeActionList(actionDescription):
			actionList=[]
			for description in actionDescription.split(","):
				action=StrokeAction.fromDescription(description)
				actionList.append(action)
			return actionList

		newExp = strokeObject.getNewExpression()
		strokeName = strokeObject.getName()
		actionList = parseStrokeActionList(newExp)

		strokeInfo=StrokeInfo(contourPane, strokeName, actionList)
		return Stroke(strokeInfo, StrokeState())

	def clone(self):
		return Stroke(self.strokeInfo, self.state.clone())

	def getTypeName(self):
		return self.strokeInfo.getTypeName()

	def getCode(self):
		newContourPane=self.strokeInfo.contourPane.clone()
		self.state.getTargetPane().transformPane(newContourPane)

		codeList=self.strokeInfo.getCodeList(newContourPane)
		return ','.join(codeList)

	# 多型
	def transform(self, pane):
		pane.transformPane(self.state.getTargetPane())

	@staticmethod
	def parseStrokeInfo(strokeExpression):
		l=strokeExpression.split(';')
		name=l[0]
		scopeDesc=l[1]

		left=int(scopeDesc[0:2], 16)
		top=int(scopeDesc[2:4], 16)
		right=int(scopeDesc[4:6], 16)
		bottom=int(scopeDesc[6:8], 16)
		scope=(left, top, right, bottom)

		strokeDesc=l[2]
		parameterExpression = strokeDesc[1:-1]
		parameterExpressionList = parameterExpression.split(',')

		clsStrokeObject = StrokeObjectMap.get(name, None)
		assert clsStrokeObject!=None
		return clsStrokeObject(name, scope, parameterExpressionList)

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

	def getCode(self):
		strokeList=self.getStrokeList()
		codeList=[stroke.getCode() for stroke in strokeList]
		return ','.join(codeList)

	# 多型
	def transform(self, pane):
		for stroke in self.strokeList:
			stroke.transform(pane)

