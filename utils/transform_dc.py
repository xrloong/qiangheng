
import re


def main():
	filename="qhdata/radix/CJK/dc.xml"
#	filename="qhdata/radix/CJK-A/dc.xml"

	pattern = '(.*)資訊表示式="\((.*)\)(.*)"(.*)'
	r=re.compile(pattern)
	for line in open(filename):
		l = line.strip('\n')
		sre=r.search(l)
		if sre:
			pre=sre.group(1)
			name=sre.group(2)
			exp=sre.group(3)
			post=sre.group(4)
#			print('%s資訊表示式="(%s)%s"%s'%(pre, name, exp, post))
#			print('{0}資訊表示式="({1}){2}"{3}'.format(pre, name, exp, post))
			genStroke(name, exp)
#		else:
#			print(l)

def main():
	pattern = '(.*)資訊表示式="\((.*)\)(.*)"(.*)'
	r=re.compile(pattern)
	for filename in ["qhdata/radix/CJK/dc.xml", "qhdata/radix/CJK-A/dc.xml", ]:
		for line in open(filename):
			l = line.strip('\n')
			sre=r.search(l)
			if sre:
				pre=sre.group(1)
				name=sre.group(2)
				exp=sre.group(3)
				post=sre.group(4)
				genStroke(name, exp)

class BaseCurveComputer:
	def __init__(self, name, exp):
		def getAction(e):
			return e[:4]

		self.name = name
		self.exp = exp
		self.pointList = exp.split(',')
		self.actionList = list(map(getAction, self.pointList))

		self.checkType()

		self.genStartEnd()
		self.genScope()

		self.scopeWidth = self.scope[2] - self.scope[0]
		self.scopeHeight = self.scope[3] - self.scope[1]
		self.strokeWidth = self.scopeWidth - 2
		self.strokeHeight = self.scopeHeight - 2

		self.genInfo()
		self.genNewExp()
		self.genNewScope()

	def getErrorInfo(self):
		return "Expreesion Error: %s %s"%(self.name, self.exp)

	def checkType(self):
		assert True, "Type error: {0} {1}".format(self.name, self.exp)

	def computeScope(self, x, y):
		return [x-1, y-1, x+1, y+1]

	def mergeScope(self, scope1, scope2):
		return [min(scope1[0], scope2[0]),
			min(scope1[1], scope2[1]),
			max(scope1[2], scope2[2]),
			max(scope1[3], scope2[3])]

	def getPos(self, exp):
		return [int(exp[4:6], 16), int(exp[6:8], 16)]

	def genStartEnd(self):
		startEnd = [0, 0, 0, 0]
		if len(self.pointList) >= 2:
			startEnd = [
				int(self.pointList[0][4:6], 16),
				int(self.pointList[0][6:8], 16),
				int(self.pointList[-1][4:6], 16),
				int(self.pointList[-1][6:8], 16),
				]
		self.startEnd = startEnd

	def computeScope(self, expressionList):
		def solve(x0, x1, x2, x):
			a=x0-2*x1+x2		# y0-2y1+y2
			b=2*(x1-x0)		# -2(y1-y0)
			c=x0-x			# -2(y0-y)
			solutions=[]
			if a!=0:
				b2_4ac=b*b-4*a*c
				if b2_4ac>=0:
					tmp=b2_4ac**0.5
					solutions=[(-b+tmp)/(2*a), (-b-tmp)/(2*a)]
				else:
					solutions=[]
			else:
				t=c/(-2*b)
				solutions=[t]
			return solutions

		def getPos(exp):
			return [int(exp[4:6], 16), int(exp[6:8], 16)]

		def findLeft(expressionList):
			pointList = map(lambda p: getPos(p), expressionList)
			start = min(list(zip(*pointList))[0])
			end = 0
			for x in range(start, end -1, -1):
				prevPoint = getPos(expressionList[0])
				midPoint = None
				for p in expressionList[1:]:
					currPoint = getPos(p)

					if p[0:4]=='0001':
						withSolution=True
						if midPoint:
							solution=solve(prevPoint[0], midPoint[0], currPoint[0], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[0], currPoint[0]) <= x <= max(prevPoint[0], currPoint[0])
						if withSolution: break

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
				else:
					# it pass all case of for, it means it doesn't find solution
					return x
			return 0

		def findRight(expressionList):
			pointList = map(lambda p: getPos(p), expressionList)
			start = max(list(zip(*pointList))[0])
			end = 0xFF
			for x in range(start, end + 1):
				prevPoint = getPos(expressionList[0])
				midPoint = None
				for p in expressionList[1:]:
					currPoint = getPos(p)

					if p[0:4]=='0001':
						withSolution=False
						if midPoint:
							solution=solve(prevPoint[0], midPoint[0], currPoint[0], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[0], currPoint[0]) <= x <= max(prevPoint[0], currPoint[0])
						if withSolution: break

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
				else:
					# it pass all case of for, it means it doesn't find solution
					return x
			return 0xFF

		def findTop(expressionList):
			pointList = map(lambda p: getPos(p), expressionList)
			start = min(list(zip(*pointList))[1])
			end = 0
			for x in range(start, end -1, -1):
				prevPoint = getPos(expressionList[0])
				midPoint = None
				for p in expressionList[1:]:
					currPoint = getPos(p)

					if p[0:4]=='0001':
						withSolution=False
						if midPoint:
							solution=solve(prevPoint[1], midPoint[1], currPoint[1], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[1], currPoint[1]) <= x <= max(prevPoint[1], currPoint[1])
						if withSolution: break

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
				else:
					# it pass all case of for, it means it doesn't find solution
					return x
			return 0

		def findBottom(expressionList):
			pointList = map(lambda p: getPos(p), expressionList)
			start = max(list(zip(*pointList))[1])
			end = 0xFF
			for x in range(start, end + 1):
				prevPoint = getPos(expressionList[0])
				midPoint = None
				for p in expressionList[1:]:
					currPoint = getPos(p)

					if p[0:4]=='0001':
						withSolution=False
						if midPoint:
							solution=solve(prevPoint[1], midPoint[1], currPoint[1], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[1], currPoint[1]) <= x <= max(prevPoint[1], currPoint[1])
						if withSolution: break

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
				else:
					# it pass all case of for, it means it doesn't find solution
					return x
			return 0xFF
		scope = [
			findLeft(expressionList),
			findTop(expressionList),
			findRight(expressionList),
			findBottom(expressionList),
			]
		return scope

	def genScope(self):
		expressionList=self.pointList
		self.scope = self.computeScope(expressionList)

	def genNewScope(self):
		expressionList=self.newExp.split(",")
		self.newScope = self.computeScope(expressionList)

	def getNewScope(self):
		return self.newScope

	def getStartPoint(self):
		return self.getStartEnd()[:2]

	def getStartPointAtTopLeft(self):
		left, top, right, bottom = self.getScope()
		return [left + 1, top + 1]

	def getStartPointAtTopRight(self):
		left, top, right, bottom = self.getScope()
		return [right - 1, top + 1]

	def getStartPointAtBottomLeft(self):
		left, top, right, bottom = self.getScope()
		return [left + 1, bottom - 1]

	def getStartPointAtBottomRight(self):
		left, top, right, bottom = self.getScope()
		return [right - 1, bottom - 1]

	def genStrokeString(self, pointInfoList):
		startPoint = pointInfoList[0]
		strokeStringList = ["0000{0[0]:02X}{0[1]:02X}".format(startPoint[1])]
		isCurveControl = False
		for point in pointInfoList[1:]:
			isCurveControl = point[0]
			if isCurveControl:
				s = "0002{0[0]:02X}{0[1]:02X}".format(point[1])
			else:
				s = "0001{0[0]:02X}{0[1]:02X}".format(point[1])
			strokeStringList.append(s)

		assert not isCurveControl, "Wrong data {0}".format(pointInfoList)
		return ",".join(strokeStringList)

	def genInfo(self):
		self.info=""

	def genNewExp(self):
		self.newExp=""

	def getStartEnd(self):
		return self.startEnd

	def getScopeWidth(self):
		return self.scopeWidth

	def getScopeHeight(self):
		return self.scopeHeight

	def getStrokeWidth(self):
		return self.strokeWidth

	def getStrokeHeight(self):
		return self.strokeHeight

	def getScope(self):
		return self.scope

	def getInfo(self):
		return self.info

	def getNewExp(self):
		return self.newExp

	def get_點(self, startPoint, width, height):
		assert height>0
		return [(False, (startPoint[0] + width, startPoint[1] + height))]

	def get_圓(self, startPoint, a, b):
		assert a>0 and b>0
		CX = startPoint[0]
		CY = startPoint[1] + b

		topLeftPoint = [CX - a, CY - b]
		topPoint = [CX, CY - b]
		topRightPoint = [CX + a, CY - b]
		bottomLeftPoint = [CX - a, CY + b]
		bottomPoint = [CX, CY + b]
		bottomRightPoint = [CX + a, CY + b]
		leftPoint = [CX - a, CY]
		rightPoint = [CX + a, CY]

		return [
			(False, topPoint), (True, topRightPoint), (False, rightPoint),
			(True, bottomRightPoint), (False, bottomPoint), (True, bottomLeftPoint),
			(False, leftPoint), (True, topLeftPoint), (False, topPoint)
			]

	def get_橫(self, startPoint, width):
		assert width>0
		return [(False, (startPoint[0] + width, startPoint[1]))]

	def get_豎(self, startPoint, height):
		assert height>0
		return [(False, (startPoint[0], startPoint[1] + height))]

	def get_左(self, startPoint, width):
		assert width>0
		return [ (False, (startPoint[0] - width, startPoint[1])), ]

	def get_上(self, startPoint, height):
		assert height>0
		return [ (False, (startPoint[0], startPoint[1] - height)), ]

	def get_提(self, startPoint, width, height):
		assert width>0 and height>0
		return [(False, (startPoint[0] + width, startPoint[1] - height))]

	def get_捺(self, startPoint, width, height):
		assert width>0 and height>0
		cPoint = [startPoint[0] + width//2, startPoint[1] + height//2]
		midPoint = [max(0, cPoint[0] - height//3), min(0xFF, cPoint[1] + width//3)]
		endPoint = [startPoint[0] + width, startPoint[1] + height]
		return [(True, (midPoint[0], midPoint[1])),
			(False, (endPoint[0], endPoint[1])), ]

	def get_撇(self, startPoint, width, height):
#		if not (width>0 and height>0): print(self.exp)
#		assert (width>=0 and height>0)
		return [(False, (startPoint[0] - width, startPoint[1] + height))]

	def get_趯(self, startPoint, width, height):
		assert width>0 and height>0
		return [ (False, (startPoint[0] - width, startPoint[1] - height)), ]


	def get_臥捺(self, startPoint, w, h):
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

	def get_豎撇(self, startPoint, w, h):
		assert w>0 and h>0
		tmph = h - h//2

		startPoint = self.getStartPoint()
		midPoint1 = [startPoint[0], startPoint[1] + tmph]
		midPoint2 = [startPoint[0], startPoint[1] + h]
		endPoint = [startPoint[0] - w, startPoint[1] + h]

		return [ (False, midPoint1), (True, midPoint2), (False, endPoint) ]

	def get_豎鉤之豎(self, startPoint, h1, h2, w):
		assert h1>0 and h2 and w>0
		midPoint1 = [startPoint[0], startPoint[1] + h1 - h2*2]
		midPoint2 = [startPoint[0], startPoint[1] + h1 + h2]
		midPoint3 = [midPoint2[0] - w//4, midPoint2[1]]
		return [(False, midPoint1),
			(True, midPoint2),
			(False, midPoint3), ]

	def get_彎鉤之彎(self, startPoint, w1, h1):
		assert h1>0
		cPoint = [startPoint[0] + w1//2, startPoint[1] + h1//2]
		midPoint1 = [min(0xFF, cPoint[0] + h1//2), max(0, cPoint[1] - w1//2)]
		midPoint2 = [startPoint[0] + w1, startPoint[1] + h1]
		return [(True, midPoint1),
			(False, midPoint2),
			]

	def get_撇鉤之撇(self, startPoint, w, h):
		assert w>0 and h>0
		return [(True, (startPoint[0], startPoint[1] + h)),
			(False, (startPoint[0] - w, startPoint[1] + h)),
			]

	def get_斜鉤之斜(self, startPoint, w, h):
		assert w>0 and h>0
		return [(True, (startPoint[0] + w//5, startPoint[1] + h*4//5)),
			(False, (startPoint[0] + w, startPoint[1] + h)),
			]

	def get_曲(self, startPoint, cr):
		assert cr>0
		return [ (True, (startPoint[0], startPoint[1] + cr)), (False, (startPoint[0] + cr, startPoint[1] + cr)),]

	def get_撇曲(self, startPoint, wl, wr, h):
		assert wl>0 and wr>0 and h>0
		midPoint2 = [startPoint[0] - wl, startPoint[1] + h]

		cr = 0x30
		tmp = cr

		midPoint1 = [midPoint2[0] + tmp, startPoint[1] + (wl - tmp) * h // wl]
		midPoint3 = [midPoint2[0] + tmp, startPoint[1] + h]
		midPoint4 = [startPoint[0] + wr , startPoint[1] + h]

		return [ (False, midPoint1), (True, midPoint2), (False, midPoint3), (False, midPoint4), ]

class InvalidCurveComputer(BaseCurveComputer):
	def checkType(self):
		assert False, "Type error: {0}".format(self.getErrorInfo())

class CurveComputer_點(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001'], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		endX, endY = self.getPos(pointList[1]) 
#		assert startX < endX and startY < endY, "Error: {0}".format(self.getErrorInfo())
		assert startY < endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[1])
		self.info = [endX - startX, endY - startY]

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_點(pointInfoList[-1][1], w, h))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001'], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		endX, endY = self.getPos(pointList[1]) 
		assert startY==endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		left, top, right, bottom = self.getScope()

		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[1])
		w = min(endX - startX, self.getStrokeWidth())

		self.info = [w]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		l = self.getInfo()[0]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], l))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		midX, midY = self.getPos(pointList[1]) 
		endX, endY = self.getPos(pointList[2]) 
		assert startY==midY, "Error: {0}".format(self.getErrorInfo())
		assert midX>endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		left, top, right, bottom = self.getScope()

		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[1])
		endX, endY = self.getPos(self.pointList[2])

		w = min(midX - startX, self.getStrokeWidth())
		wg = midX - endX
		hg = min(endY - midY, self.getStrokeHeight())
		self.info = [w, wg, hg]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		wp = self.getInfo()[1]
		hp = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], wp, hp))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫折(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		midX, midY = self.getPos(pointList[1]) 
		endX, endY = self.getPos(pointList[2]) 
		assert startY==midY, "Error: {0}".format(self.getErrorInfo())
		assert midX==endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		left, top, right, bottom = self.getScope()

		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[1])
		endX, endY = self.getPos(self.pointList[2])

		w = min(midX - startX, self.getStrokeWidth())
		h = min(endY - midY, self.getStrokeHeight())
		self.info = [w, h]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		hl = self.getInfo()[0]
		wl = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], hl))
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], wl))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫折橫(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		mid1X, mid1Y = self.getPos(pointList[1]) 
		mid2X, mid2Y = self.getPos(pointList[2]) 
		endX, endY = self.getPos(pointList[3]) 
		assert startY==mid1Y, "Error: {0}".format(self.getErrorInfo())
		assert mid1X==mid2X, "Error: {0}".format(self.getErrorInfo())
		assert mid2Y==endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		left, top, right, bottom = self.getScope()

		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[3])

		w2 = endX - mid2X
		w = min(mid1X - startX, self.getStrokeWidth() - w2)
		h = min(mid2Y - mid1Y, self.getStrokeHeight())
		self.info = [w, h, w2]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w1l = self.getInfo()[0]
		hl = self.getInfo()[1]
		w2l = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w1l))
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], hl))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w2l))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫折提(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		mid1X, mid1Y = self.getPos(pointList[1]) 
		mid2X, mid2Y = self.getPos(pointList[2]) 
		endX, endY = self.getPos(pointList[3]) 
		assert startY==mid1Y, "Error: {0}".format(self.getErrorInfo())
		assert mid1X==mid2X, "Error: {0}".format(self.getErrorInfo())
		assert mid2Y>endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[3])

		wt = endX - mid2X
		ht = mid2Y - endY
		w = min(mid1X - startX, self.getStrokeWidth() - wt)
		h = min(mid2Y - mid1Y, self.getStrokeHeight())
		self.info = [w, h, wt, ht]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		wt = self.getInfo()[2]
		ht = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], h))
		pointInfoList.extend(self.get_提(pointInfoList[-1][1], wt, ht))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫折鉤(BaseCurveComputer):
	def checkType(self):
		assert len(self.actionList)>=4, "Error: {0}".format(self.getErrorInfo())
#		assert self.actionList==['0000', '0001', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		mid1X, mid1Y = self.getPos(pointList[1]) 
		mid2X, mid2Y = self.getPos(pointList[-2]) 
		endX, endY = self.getPos(pointList[-1]) 
#		assert startY==mid1Y, "Error: {0}".format(self.getErrorInfo())
#		if not startY==mid1Y: print("Error: {0}".format(self.getErrorInfo()))
		assert mid1X>=mid2X, "Error: {0}".format(self.getErrorInfo())
		assert mid2X>endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		w = min(mid1X - startX, self.getStrokeWidth())
		h = min(mid2Y - startY, self.getStrokeHeight())
		wg = mid1X - endX
		hg = mid2X - endX
		self.info = [w, h, wg, hg]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		wg = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇鉤之撇(pointInfoList[-1][1], wg//2, h))
		pointInfoList.extend(self.get_趯(pointInfoList[-1][1], wg//2, hg))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫折彎鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0002', '0001', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])

		curveStartX, curveStartY = self.getPos(self.pointList[2])
		curveX, curveY = self.getPos(self.pointList[3])
		curveEndX, curveEndY = self.getPos(self.pointList[4])

		cr = min(curveY - curveStartY, curveEndX - curveX)
		hl = min(curveY - mid1Y, self.getStrokeHeight())
		wl = mid2X - curveX
		w = min(mid1X - startX, self.getStrokeWidth() - wl)

		tl = mid2Y - endY
		self.info = [w, hl, wl, cr, tl]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		hl = self.getInfo()[1]
		wl = self.getInfo()[2]
		cr = self.getInfo()[3]
		tl = self.getInfo()[4]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], hl - cr))
		pointInfoList.extend(self.get_曲(pointInfoList[-1][1], cr))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], wl - cr))
		pointInfoList.extend(self.get_上(pointInfoList[-1][1], tl))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫撇(BaseCurveComputer):
	def checkType(self):
		pass

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[1])
		endX, endY = self.getPos(self.pointList[-1])
		w = min(midX - startX, self.getStrokeWidth())
		wp = min(midX - endX, self.getStrokeWidth())
		hp = min(endY - midY, self.getStrokeHeight())
		self.info = [w, wp, hp]

	def getStartPoint(self):
		w = self.getInfo()[0]
		wp = self.getInfo()[1]
		hp = self.getInfo()[2]
		topLeft = self.getStartPointAtTopLeft()
		if w > wp:
			return topLeft
		else:
			return (topLeft[0]+(wp-w), topLeft[1])

	def genNewExp(self):
		w = self.getInfo()[0]
		wp = self.getInfo()[1]
		hp = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], wp, hp))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫撇彎鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0002', '0001', '0002', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		tmpX, tmpY = self.getPos(self.pointList[3])
		mid2X, mid2Y = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		w = mid1X - startX
		h = min((mid2Y - startY), self.getStrokeHeight())
		wb = min(mid1X - tmpX, self.getStrokeWidth())
		t = mid2Y - endY
		self.info = [w, h, wb, t]

	def getStartPoint(self):
		left, top, right, bottom = self.getScope()

		w = self.getInfo()[0]
		wb = self.getInfo()[2]

		leftTop = self.getStartPointAtTopLeft()
		sX = leftTop[0] + (wb-w)//2
		sY = leftTop[1]
		return (sX, sY)

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		wb = self.getInfo()[2]
		t = self.getInfo()[3]

		wr = (wb-w)//2
		wl = wb - wr

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇曲(pointInfoList[-1][1], wl, wr, h))
		pointInfoList.extend(self.get_上(pointInfoList[-1][1], t))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫撇橫折鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0001', '0002', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		mid1X, mid1Y = self.getPos(pointList[1]) 
		mid2X, mid2Y = self.getPos(pointList[-2]) 
		endX, endY = self.getPos(pointList[-1]) 
		assert startX<endX and startY==mid1Y, "Error: {0}".format(self.getErrorInfo())
		assert mid1X>=mid2X and mid1Y<mid2Y, "Error: {0}".format(self.getErrorInfo())
#		assert mid2X>endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		mid3X, mid3Y = self.getPos(self.pointList[3])
		mid4X, mid4Y = self.getPos(self.pointList[4])
		mid5X, mid5Y = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		w = mid1X - startX
		w2 = mid1X - mid2X
		h2 = mid2Y - mid1Y
		w3 = mid3X - mid2X
		hh = mid5Y - mid3Y
		wg = mid3X - endX
		hg = mid5Y - endY
		self.info = [w, w2, h2, w3, hh, wg, hg]

	def genNewExp(self):
		w = self.getInfo()[0]
		w2 = self.getInfo()[1]
		h2 = self.getInfo()[2]
		w3 = self.getInfo()[3]
		hh = self.getInfo()[4]
		wg = self.getInfo()[5]
		hg = self.getInfo()[6]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], w2, h2))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w3))
		pointInfoList.extend(self.get_撇鉤之撇(pointInfoList[-1][1], wg//2, hh))
		pointInfoList.extend(self.get_趯(pointInfoList[-1][1], wg//2, hg))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫斜鉤(BaseCurveComputer):
	def checkType(self):
		assert len(self.actionList)>=5, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])

		w2 = mid2X - mid1X
		h2 = min(mid2Y - mid1Y, self.getStrokeHeight())

		w = min(mid1X - startX, self.getStrokeWidth() - w2)

		hg = mid2Y - endY
		self.info = [w, w2, h2, hg]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		w2 = self.getInfo()[1]
		h2 = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_斜鉤之斜(pointInfoList[-1][1], w2, h2))
		pointInfoList.extend(self.get_上(pointInfoList[-1][1], hg))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫折橫折(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		mid1X, mid1Y = self.getPos(pointList[1]) 
		mid2X, mid2Y = self.getPos(pointList[2]) 
		mid3X, mid3Y = self.getPos(pointList[3]) 
		endX, endY = self.getPos(pointList[4]) 
		assert startY==mid1Y, "Error: {0}".format(self.getErrorInfo())
		assert mid1X==mid2X, "Error: {0}".format(self.getErrorInfo())
		assert mid2Y==mid3Y, "Error: {0}".format(self.getErrorInfo())
		assert mid3X==endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		mid3X, mid3Y = self.getPos(self.pointList[3])
		endX, endY = self.getPos(self.pointList[4])

		w2 = mid3X - mid2X
		h2 = endY - mid3Y
		w1 = min(mid1X - startX, self.getStrokeWidth() - w2)
		h1 = min(mid2Y - mid1Y, self.getStrokeHeight() - h2)
		self.info = [mid1X - startX, mid2Y - mid1Y, mid3X - mid2X, endY-mid3Y]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w1l = self.getInfo()[0]
		h1l = self.getInfo()[1]
		w2l = self.getInfo()[2]
		h2l = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w1l))
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], h1l))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w2l))
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], h2l))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_豎(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001'], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		endX, endY = self.getPos(pointList[1]) 
		assert startX==endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[1])

		h = min(endY - startY, self.getStrokeHeight())
		self.info = [h]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		l = self.getInfo()[0]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], l))
		self.newExp = self.genStrokeString(pointInfoList)


class CurveComputer_豎折(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		midX, midY = self.getPos(pointList[1]) 
		endX, endY = self.getPos(pointList[2]) 
		assert startX==midX, "Error: {0}".format(self.getErrorInfo())
		assert midY==endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[1])
		endX, endY = self.getPos(self.pointList[2])

		h = min(midY - startY, self.getStrokeHeight())
		w = min(endX - midX, self.getStrokeWidth())
		self.info = [h, w]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		hl = self.getInfo()[0]
		wl = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], hl))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], wl))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_豎挑(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		midX, midY = self.getPos(pointList[1]) 
		endX, endY = self.getPos(pointList[2]) 
		assert startX==midX, "Error: {0}".format(self.getErrorInfo())
		assert midX<endX and midY>endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[1])
		endX, endY = self.getPos(self.pointList[2])

		h = min(midY - startY, self.getStrokeHeight())
		wt = min(endX - midX, self.getStrokeWidth())
		ht = midY - endY
		self.info = [h, wt, ht]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		h = self.getInfo()[0]
		wt = self.getInfo()[1]
		ht = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], h))
		pointInfoList.extend(self.get_提(pointInfoList[-1][1], wt, ht))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_豎橫折(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		mid1X, mid1Y = self.getPos(pointList[1]) 
		mid2X, mid2Y = self.getPos(pointList[2]) 
		endX, endY = self.getPos(pointList[3]) 
		assert startX==mid1X, "Error: {0}".format(self.getErrorInfo())
		assert mid1Y==mid2Y, "Error: {0}".format(self.getErrorInfo())
		assert mid2X==endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[3])

		h2 = endY - mid2Y
		h = min(mid1Y - startY, self.getStrokeHeight() - h2)
		w = min(mid2X - mid1X, self.getStrokeWidth())
		self.info = [h, w, h2]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		h1l = self.getInfo()[0]
		wl = self.getInfo()[1]
		h2l = self.getInfo()[2]
		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], h1l))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], wl))
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], h2l))
		self.newExp = self.genStrokeString(pointInfoList)


class CurveComputer_豎橫折鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0001', '0002', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		mid1X, mid1Y = self.getPos(pointList[1]) 
		mid2X, mid2Y = self.getPos(pointList[2]) 
		mid3X, mid3Y = self.getPos(pointList[3]) 
		mid4X, mid4Y = self.getPos(pointList[4]) 
		endX, endY = self.getPos(pointList[5]) 
#		assert startX==mid1X, "Error: {0}".format(self.getErrorInfo())
		assert mid1Y==mid2Y, "Error: {0}".format(self.getErrorInfo())
#		assert mid2X==endX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		mid3X, mid3Y = self.getPos(self.pointList[3])
		mid4X, mid4Y = self.getPos(self.pointList[4])
		endX, endY = self.getPos(self.pointList[5])
		wp = startX - mid1X
		hp = mid1Y - startY
		w = mid2X - mid1X
		h = mid4Y - mid2Y
		wg = mid2X - endX
		hg = mid4Y - endY
		self.info = [wp, hp, w, h, wg, hg]

	def genNewExp(self):
		wp = self.getInfo()[0]
		hp = self.getInfo()[1]
		w = self.getInfo()[2]
		h = self.getInfo()[3]
		wg = self.getInfo()[4]
		hg = self.getInfo()[5]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		if wp>0:
			pointInfoList.extend(self.get_撇(pointInfoList[-1][1], wp, hp))
		elif wp<0:
			#捺
			assert False
		else:
			pointInfoList.extend(self.get_豎(pointInfoList[-1][1], hp))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇鉤之撇(pointInfoList[-1][1], wg//2, h))
		pointInfoList.extend(self.get_趯(pointInfoList[-1][1], wg//2, hg))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_豎曲鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList[2]=='0002', "Error: {0}".format(self.getErrorInfo())
		preEndX, preEndY = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		assert endX==preEndX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		preEndX, preEndY = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])

		curveStartX, curveStartY = self.getPos(self.pointList[1])
		curveX, curveY = self.getPos(self.pointList[2])
		curveEndX, curveEndY = self.getPos(self.pointList[3])

		hl = curveY - startY
		wl = endX - curveX
		cr = min(curveY - curveStartY, curveEndX - curveX)
		tl = preEndY - endY

		w = min(preEndX - startX, self.getStrokeWidth()) - cr
		h = min(preEndY - startY, self.getStrokeHeight()) - cr
		self.info = [h, w, cr, tl]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		hl = self.getInfo()[0]
		wl = self.getInfo()[1]
		cr = self.getInfo()[2]
		tl = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], hl - cr))
		pointInfoList.extend(self.get_曲(pointInfoList[-1][1], cr))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], wl - cr))
		pointInfoList.extend(self.get_上(pointInfoList[-1][1], tl))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_豎曲(BaseCurveComputer):
	def checkType(self):
		pass
#		assert self.actionList[2]=='0002', "Error: {0}".format(self.getErrorInfo())
#		preEndX, preEndY = self.getPos(self.pointList[-2])
#		endX, endY = self.getPos(self.pointList[-1])
#		assert endX==preEndX, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[-1])

		cr = min((endX - startX)//3, (endY - startY)//3, 0x20)
		w = min(endX - startX, self.getStrokeWidth()) - cr
		h = min(endY - startY, self.getStrokeHeight()) - cr
		self.info = [w, h, cr]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		cr = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], h))
		pointInfoList.extend(self.get_曲(pointInfoList[-1][1], cr))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_豎鉤(BaseCurveComputer):
	def checkType(self):
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		w=startX-endX
		h1=endY-startY
		h2=midY-endY
		assert h1-h2*2>0, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])

		h = min(midY - startY, self.getStrokeHeight())
		wg = min(startX - endX, self.getStrokeWidth())
		hg = midY-endY

		self.info = [h, wg, hg]

	def getStartPoint(self):
		return self.getStartPointAtTopRight()

	def genNewExp(self):
		h = self.getInfo()[0]
		wg = self.getInfo()[1]
		hg = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎鉤之豎(pointInfoList[-1][1], h-hg, hg, wg))
		pointInfoList.extend(self.get_趯(pointInfoList[-1][1], wg//2, wg//2))
		self.newExp = self.genStrokeString(pointInfoList)


class CurveComputer_斜鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0002', '0001', '0001'], "Error: {0}".format(self.getErrorInfo())
#		startX, startY = self.getPos(self.pointList[0])
#		midX, midY = self.getPos(self.pointList[-2])
#		endX, endY = self.getPos(self.pointList[-1])
#		w=startX-endX
#		h1=endY-startY
#		h2=midY-endY
#		assert h1-h2*2>0, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[3])

		cr = min((endX - startX)//3, (endY - startY)//3, 0x20)
		w = min(mid2X - startX, self.getStrokeWidth())
		h = min(mid2Y - startY, self.getStrokeHeight())
		ht=mid2Y-endY
		self.info = [w, h, ht]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		ht = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_斜鉤之斜(pointInfoList[-1][1], w, h))
		pointInfoList.extend(self.get_上(pointInfoList[-1][1], ht))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_彎鉤(BaseCurveComputer):
	def checkType(self):
		pass
#		startX, startY = self.getPos(self.pointList[0])
#		midX, midY = self.getPos(self.pointList[-2])
#		endX, endY = self.getPos(self.pointList[-1])
#		w=startX-endX
#		h1=endY-startY
#		h2=midY-endY
#		assert h1-h2*2>0, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		w1=midX-startX
		h1=midY-startY
		wg=midX-endX
		hg=midY-endY
		self.info = [w1, h1, wg, hg]

	def genNewExp(self):
		w1 = self.getInfo()[0]
		h1 = self.getInfo()[1]
		wg = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_彎鉤之彎(pointInfoList[-1][1], w1, h1))
		pointInfoList.extend(self.get_趯(pointInfoList[-1][1], wg, hg))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_撇鉤(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0002', '0001', '0001', ], "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		wp=midX-startX
		hp=midY-startY
		wg=midX-endX
		hg=midY-endY
		self.info = [wp, hp, wg, hg]

	def genNewExp(self):
		wp = self.getInfo()[0]
		hp = self.getInfo()[1]
		wg = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_彎鉤之彎(pointInfoList[-1][1], wp, hp))
		pointInfoList.extend(self.get_趯(pointInfoList[-1][1], wg, hg))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_捺(BaseCurveComputer):
	def checkType(self):
		pass

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[-1])
		w=endX-startX
		h=endY-startY
		self.info = [w, h]

		w = min(endX - startX, self.getStrokeWidth())
		h = min(endY - startY, self.getStrokeHeight())
		self.info = [w, h]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_捺(pointInfoList[-1][1], w, h))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_撇(BaseCurveComputer):
	def checkType(self):
		pass

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[-1])
		w = min(startX - endX, self.getStrokeWidth())
		h = min(endY - startY, self.getStrokeHeight())
		self.info = [w, h]

	def getStartPoint(self):
		return self.getStartPointAtTopRight()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], w, h))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_撇頓點(BaseCurveComputer):
	def checkType(self):
		assert len(self.actionList)>=3, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		i = self.actionList[1:-1].index("0001")+1
		midX, midY = self.getPos(self.pointList[i])
		endX, endY = self.getPos(self.pointList[-1])

		w2 = min(endX - midX, self.getStrokeWidth())
		h2 = endY - midY

		w1 = min(startX - midX, self.getStrokeWidth())
		h1 = min(midY - startY, self.getStrokeHeight() - h2)
		self.info = [w1, h1, w2, h2]

	def getStartPoint(self):
		topRight = self.getStartPointAtTopRight()
		w1 = self.getInfo()[0]
		h1 = self.getInfo()[1]
		w2 = self.getInfo()[2]
		h2 = self.getInfo()[3]

		if w1 > w2:
			return topRight
		else:
			return (topRight[0] - (w2-w1), topRight[1])

	def genNewExp(self):
		w1 = self.getInfo()[0]
		h1 = self.getInfo()[1]
		w2 = self.getInfo()[2]
		h2 = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], w1, h1))
		pointInfoList.extend(self.get_點(pointInfoList[-1][1], w2, h2))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_撇橫(BaseCurveComputer):
	def checkType(self):
		assert len(self.actionList)>=3, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		i = self.actionList[1:-1].index("0001")+1
		midX, midY = self.getPos(self.pointList[i])
		endX, endY = self.getPos(self.pointList[-1])
		w1 = startX - midX
		h1 = midY - startY
		w2 = endX - midX
		h2 = endY - midY
		self.info = [w1, h1, w2, h2]

	def genNewExp(self):
		w1 = self.getInfo()[0]
		h1 = self.getInfo()[1]
		w2 = self.getInfo()[2]
		h2 = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], w1, h1))
		if h2>0:
			pointInfoList.extend(self.get_點(pointInfoList[-1][1], w2, h2))
		elif h2<0:
			pointInfoList.extend(self.get_提(pointInfoList[-1][1], w2, -h2))
		else:
			pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w2))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_撇橫撇(BaseCurveComputer):
	def checkType(self):
		assert len(self.actionList)>=3, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[-1])
		w1 = startX - mid1X
		h1 = mid1Y - startY
		w = mid2X - mid1X
		w2 = mid2X - endX
		h2 = endY - mid2Y
		self.info = [w1, h1, w, w2, h2]

	def genNewExp(self):
		w1 = self.getInfo()[0]
		h1 = self.getInfo()[1]
		w = self.getInfo()[2]
		w2 = self.getInfo()[3]
		h2 = self.getInfo()[4]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], w1, h1))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇(pointInfoList[-1][1], w2, h2))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_豎撇(BaseCurveComputer):
	def checkType(self):
		assert len(self.actionList)>=3, "Error: {0}".format(self.getErrorInfo())
		assert self.actionList[-2]=='0002', "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		endX, endY = self.getPos(pointList[-1]) 
		assert startX > endX and startY < endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[-1])
		w = min(startX - endX, self.getStrokeWidth())
		h = min(endY - startY, self.getStrokeHeight())
		self.info = [w, h]

	def getStartPoint(self):
		return self.getStartPointAtTopRight()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎撇(pointInfoList[-1][1], w, h))
		self.newExp = self.genStrokeString(pointInfoList)


class CurveComputer_挑(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001'], "Error: {0}".format(self.getErrorInfo())

		pointList = self.pointList
		startX, startY = self.getPos(pointList[0]) 
		endX, endY = self.getPos(pointList[1]) 
		assert startX < endX and startY > endY, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[1])
		w = min(endX - startX, self.getStrokeWidth())
		h = min(startY - endY, self.getStrokeHeight())
		self.info = [w, h]

	def getStartPoint(self):
		return self.getStartPointAtBottomLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_提(pointInfoList[-1][1], w, h))
		self.newExp = self.genStrokeString(pointInfoList)


class CurveComputer_橫捺(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0002', '0001', ], "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[-1])
		wn = endX - mid1X
		hn = endY - mid1Y
		w = min(mid1X - startX, self.getStrokeWidth() - wn)
		self.info = [w, wn, hn]

	def getStartPoint(self):
		return self.getStartPointAtTopLeft()

	def genNewExp(self):
		w = self.getInfo()[0]
		wn = self.getInfo()[1]
		hn = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_捺(pointInfoList[-1][1], wn, hn))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_臥捺(BaseCurveComputer):
	def checkType(self):
		pass
#		assert self.actionList==['0000', '0001', '0002', '0001', ], "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[-1])
		w = endX - startX
		h = endY - startY
		self.info = [w, h]

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_臥捺(pointInfoList[-1][1], w, h))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_挑捺(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0002', '0001', ], "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[-1])
		wn = endX - mid1X
		hn = min(endY - mid1Y, self.getStrokeHeight())

		h = min(startY - mid1Y, self.getStrokeHeight())
		w = min(mid1X - startX, self.getStrokeWidth()-wn)

		self.info = [w, h, wn, hn]

	def getStartPoint(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		wn = self.getInfo()[2]
		hn = self.getInfo()[3]
		topLeft = self.getStartPointAtTopLeft()
		return (topLeft[0], topLeft[1] + h)

	def genNewExp(self):
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		wn = self.getInfo()[2]
		hn = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_提(pointInfoList[-1][1], w, h))
		pointInfoList.extend(self.get_捺(pointInfoList[-1][1], wn, hn))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_圈(BaseCurveComputer):
	def checkType(self):
		pass

	def genInfo(self):
		scope = self.getScope()
		left, top, right, bottom = scope
		self.info = [(right - left - 2)//2, (bottom - top - 2)//2]

	def getStartPoint(self):
		scope = self.getScope()
		left, top, right, bottom = scope
		CX = (left + 1) + (right-left)//2
		CY = (top + 1) + (bottom-top)//2

		a = self.getInfo()[0]
		b = self.getInfo()[1]

		startPoint = [CX, CY - b]
		return startPoint

	def genNewExp(self):
		a = self.getInfo()[0]
		b = self.getInfo()[1]

		startPoint = self.getStartPoint()
		pointInfoList = self.get_圓(startPoint, a, b)
		self.newExp = self.genStrokeString(pointInfoList)

def genStroke(name, exp):
	computerDict = {
		"點": CurveComputer_點,
		"長頓點": CurveComputer_點,
		"橫": CurveComputer_橫,
		"橫鉤": CurveComputer_橫鉤,
		"橫折": CurveComputer_橫折,
		"橫折橫": CurveComputer_橫折橫,
		"橫折提": CurveComputer_橫折提,
		"橫折鉤": CurveComputer_橫折鉤,
		"橫撇": CurveComputer_橫撇,
		"橫曲鉤": CurveComputer_橫撇彎鉤,
		"橫撇橫折鉤": CurveComputer_橫撇橫折鉤,
		"橫斜鉤": CurveComputer_橫斜鉤,
		"橫折橫折": CurveComputer_橫折橫折,
		"豎": CurveComputer_豎,
		"豎折": CurveComputer_豎折,
		"豎挑": CurveComputer_豎挑,
		"豎橫折": CurveComputer_豎橫折,
		"豎橫折鉤": CurveComputer_豎橫折鉤,
		"豎曲鉤": CurveComputer_豎曲鉤,
		"豎曲": CurveComputer_豎曲,
		"豎鉤": CurveComputer_豎鉤,
		"臥鉤": CurveComputer_豎曲鉤,
		"斜鉤": CurveComputer_斜鉤,
		"彎鉤": CurveComputer_彎鉤,
		"撇鉤": CurveComputer_撇鉤,
		"撇": CurveComputer_撇,
		"撇頓點": CurveComputer_撇頓點,
		"撇橫": CurveComputer_撇橫,
		"撇挑": CurveComputer_撇橫,
		"撇折": CurveComputer_撇橫,
		"豎撇": CurveComputer_豎撇,
		"挑": CurveComputer_挑,
#		"挑折": BaseCurveComputer,
		"捺": CurveComputer_捺,
		"臥捺": CurveComputer_臥捺,
		"挑捺": CurveComputer_挑捺,
		"橫捺": CurveComputer_橫捺,
		"圈": CurveComputer_圈,


		"撇橫撇": CurveComputer_撇橫撇,
		"橫折彎鉤": CurveComputer_橫折彎鉤,
	}
	clsComputer = computerDict.get(name, InvalidCurveComputer)
	computer = clsComputer(name, exp)
	print(
		"{0:02X}{1:02X},{2:02X}{3:02X}".format(*computer.getScope()),
		"{0:02X}{1:02X},{2:02X}{3:02X}".format(*computer.getNewScope()),
#		"{0:02X}{1:02X},{2:02X}{3:02X}".format(*computer.getStartEnd()),
		computer.getNewExp(), exp,
		computer.getInfo(),
		)

main()

#CurveComputer_點(BaseCurveComputer):
#CurveComputer_橫撇橫折鉤(BaseCurveComputer):
#CurveComputer_豎橫折鉤(BaseCurveComputer):
#CurveComputer_彎鉤(BaseCurveComputer):
#CurveComputer_撇鉤(BaseCurveComputer):
#CurveComputer_撇橫(BaseCurveComputer):
#CurveComputer_撇橫撇(BaseCurveComputer):
#CurveComputer_臥捺(BaseCurveComputer):
