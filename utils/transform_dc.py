
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
		self.genInfo()
		self.genNewExp()

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

	def findLeft(self):
		def solve(x0, x1, x2, x):
			a=x0-2*x1+x2	# y0-2y1+y2
			b=-2*(x1-x0)			# -2(y1-y0)
			c=x0-x			# -2(y0-y)
			solutions=[]
			if a!=0:
				b2_4ac=b**2-4*a*c
				if b2_4ac>=0:
					tmp=b2_4ac**0.5
					solutions=[(-b+tmp)/(2*a), (-b-tmp)/(2*a)]
				else:
					solutions=[]
			else:
				t=c/(-2*b)
				solutions=[t]
			return solutions
		for x in range(0xFF+1):
			preP = self.pointList[0]
			midP = None
			for p in self.pointList[1:]:
				prePoint = self.getPos(preP)
				currPoint = self.getPos(p)

				if p[0:4]=='0001':
					withSolution=False
					if midP:
						midPoint=self.getPos(midP)
						solution=solve(prePoint[0], midPoint[0], currPoint[0], x)
						withSolution=any(filter(lambda t: 0<=t<=1, solution))
					else:
						# line
						withSolution=min(prePoint[0], currPoint[0]) <= x <= max(prePoint[0], currPoint[0])
					if withSolution: return x;

					preP = p
					midP=None
				elif p[0:4]=='0002':
					midP=p

	def findTop(self):
		pass

	def findRight(self):
		pass

	def findBottom(self):
		pass

	def genScope(self):
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

		def findLeft(self):
			pointList = map(lambda p: self.getPos(p), self.pointList)
			start = min(list(zip(*pointList))[0])
			end = 0
			for x in range(start, end -1, -1):
				prevPoint = self.getPos(self.pointList[0])
				midPoint = None
				for p in self.pointList[1:]:
					currPoint = self.getPos(p)

					if p[0:4]=='0001':
						withSolution=False
						if midPoint:
							solution=solve(prevPoint[0], midPoint[0], currPoint[0], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[0], currPoint[0]) <= x <= max(prevPoint[0], currPoint[0])
						if not withSolution: return x;

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
			return 0

		def findRight(self):
			pointList = map(lambda p: self.getPos(p), self.pointList)
			start = max(list(zip(*pointList))[0])
			end = 0xFF
			for x in range(start, end + 1):
				prevPoint = self.getPos(self.pointList[0])
				midPoint = None
				for p in self.pointList[1:]:
					currPoint = self.getPos(p)

					if p[0:4]=='0001':
						withSolution=False
						if midPoint:
							solution=solve(prevPoint[0], midPoint[0], currPoint[0], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[0], currPoint[0]) <= x <= max(prevPoint[0], currPoint[0])
						if not withSolution: return x;

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
			return 0xFF

		def findTop(self):
			pointList = map(lambda p: self.getPos(p), self.pointList)
			start = min(list(zip(*pointList))[1])
			end = 0
			for x in range(start, end -1, -1):
				prevPoint = self.getPos(self.pointList[0])
				midPoint = None
				for p in self.pointList[1:]:
					currPoint = self.getPos(p)

					if p[0:4]=='0001':
						withSolution=False
						if midPoint:
							solution=solve(prevPoint[1], midPoint[1], currPoint[1], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[1], currPoint[1]) <= x <= max(prevPoint[1], currPoint[1])
						if not withSolution: return x;

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
			return 0

		def findBottom(self):
			pointList = map(lambda p: self.getPos(p), self.pointList)
			start = max(list(zip(*pointList))[1])
			end = 0xFF
			for x in range(start, end + 1):
				prevPoint = self.getPos(self.pointList[0])
				midPoint = None
				for p in self.pointList[1:]:
					currPoint = self.getPos(p)

					if p[0:4]=='0001':
						withSolution=False
						if midPoint:
							solution=solve(prevPoint[1], midPoint[1], currPoint[1], x)
							withSolution=any(map(lambda t: 0<=t<=1, solution))
						else:
							# line
							withSolution=min(prevPoint[1], currPoint[1]) <= x <= max(prevPoint[1], currPoint[1])
						if not withSolution: return x;

						prevPoint=currPoint
						midPoint=None
					elif p[0:4]=='0002':
						midPoint=currPoint
			return 0xFF

		self.scope = [
			findLeft(self),
			findTop(self),
			findRight(self),
			findBottom(self),
			]

	def getStartPoint(self):
		return self.getStartEnd()[:2]

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

	def getScope(self):
		return self.scope

	def getInfo(self):
		return self.info

	def getNewExp(self):
		return self.newExp

	def get_點(self, startPoint, width, height):
		return [(False, (startPoint[0] + width, startPoint[1] + height))]

	def get_圓(self, startPoint, a, b):
		CX = startPoint[0]
		CY = startPoint[1] + b

		startEnd = self.getStartEnd()
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
		return [(False, (startPoint[0] + width, startPoint[1]))]

	def get_豎(self, startPoint, height):
		return [(False, (startPoint[0], startPoint[1] + height))]

	def get_左(self, startPoint, width):
		return [ (False, (startPoint[0] - width, startPoint[1])), ]

	def get_上(self, startPoint, height):
		return [ (False, (startPoint[0], startPoint[1] - height)), ]

	def get_提(self, startPoint, width, height):
		return [(False, (startPoint[0] + width, startPoint[1] - height))]

	def get_捺(self, startPoint, width, height):
		cPoint = [startPoint[0] + width/2, startPoint[1] + height/2]
		midPoint = [max(0, int(cPoint[0] - height/3)), min(0xFF, int(cPoint[1] + width/3))]
		endPoint = [startPoint[0] + width, startPoint[1] + height]
		return [(True, (midPoint[0], midPoint[1])),
			(False, (endPoint[0], endPoint[1])), ]

	def get_撇(self, startPoint, width, height):
		return [(False, (startPoint[0] - width, startPoint[1] + height))]

	def get_趯(self, startPoint, width, height):
		return [ (False, (startPoint[0] - width, startPoint[1] - height)), ]


	def get__臥捺(self, startPoint, w, h):
		halfW = int(w/2)
		halfH = int(h/2)

		endPoint = [startPoint[0] + w, startPoint[1] + h]
		cPoint = [startPoint[0] + halfW, startPoint[1] + halfH]
		midPoint1 = [startPoint[0]+int(halfW/2)+int(halfH/4), startPoint[1]+int(halfH/2)-int(halfW/4)]
		midPoint2 = [cPoint[0]+int(halfW/2)-int(halfH/4), min(0xFF, cPoint[1]+int(halfH/2)+int(halfW/4))]
		return [(True, midPoint1),
			(False, cPoint),
			(True, midPoint2),
			(False, endPoint),]

	def get_豎鉤(self, startPoint, h1, h2, w):
		midPoint1 = [startPoint[0], startPoint[1] + h1 - h2*2]
		midPoint2 = [startPoint[0], startPoint[1] + h1 + h2]
		midPoint3 = [int(midPoint2[0] - w/4), midPoint2[1]]
		return [(False, midPoint1),
			(True, midPoint2),
			(False, midPoint3), ]

	def get_彎鉤(self, startPoint, w1, h1):
		cPoint = [startPoint[0] + w1/2, startPoint[1] + h1/2]
		midPoint1 = [min(0xFF, int(cPoint[0] + h1/2)), max(0, int(cPoint[1] - w1/2))]
		midPoint2 = [startPoint[0] + w1, startPoint[1] + h1]
		return [(True, midPoint1),
			(False, midPoint2),
			]

	def get_撇鉤(self, startPoint, h, wg, hg):
		return [(True, (startPoint[0], startPoint[1] + h)),
			(False, (startPoint[0] - int(wg/2), startPoint[1] + h)),
			(False, (startPoint[0] - wg, startPoint[1] + h - hg)),
			]

	def get_斜鉤(self, startPoint, w, h, ht):
		return [(True, (startPoint[0] + int(w/5), startPoint[1] + int(h*4/5))),
			(False, (startPoint[0] + w, startPoint[1] + h)),
			(False, (startPoint[0] + w, startPoint[1] + h - ht)),
			]

	def get_豎撇(self, startPoint, w, h):
		r = h / w / 2
		tmph = h - int(w * r)

		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		midPoint1 = [startPoint[0], startPoint[1] + tmph]
		midPoint2 = [startPoint[0], startPoint[1] + h]
		endPoint = [startPoint[0] - w, startPoint[1] + h]

		return [ (False, midPoint1), (True, midPoint2), (False, endPoint) ]

	def get_曲(self, startPoint, cr):
		return [ (True, (startPoint[0], startPoint[1] + cr)), (False, (startPoint[0] + cr, startPoint[1] + cr)),]

	def get_撇彎(self, startPoint, wl, wr, h):
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
		self.info = [endY - startY, endX - startX]

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
		startX, startY = self.getPos(self.pointList[0])
		endX, endY = self.getPos(self.pointList[1])
		self.info = [endX - startX]

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
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[1])
		endX, endY = self.getPos(self.pointList[2])
		self.info = [midX - startX, midX - endX, endY - midY]

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
		startX, startY = self.getPos(self.pointList[0])
		midX, midY = self.getPos(self.pointList[1])
		endX, endY = self.getPos(self.pointList[2])
		self.info = [midX - startX, endY - midY]

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
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[3])
		self.info = [mid1X - startX, mid2Y - mid1Y, endX - mid2X]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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
		self.info = [mid1X - startX, mid2Y - mid1Y, wt, ht]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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
		if not len(self.actionList)>=4: print("Error: {0}".format(self.getErrorInfo()))
#		assert len(self.actionList)>=2, "Error: {0}".format(self.getErrorInfo())
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
		w = mid1X - startX
		h = mid2Y - startY
		wg = mid1X - endX
		hg = mid2X - endX
		self.info = [w, h, wg, hg]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		wg = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇鉤(pointInfoList[-1][1], h, wg, hg))
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

		w = mid1X - startX
		hl = curveY - mid1Y
		wl = mid2X - curveX
		cr = min(curveY - curveStartY, curveEndX - curveX)
		tl = mid2Y - endY
		self.info = [w, hl, wl, cr, tl]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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
		w = midX - startX
		wp = midX - endX
		hp = endY - midY
		self.info = [w, wp, hp]

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
		mid2X, mid2Y = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		w = mid1X - startX
		h = (mid2Y - startY)
		wb = (mid2X - mid1X)*2+h
		t = mid2Y - endY
		self.info = [w, h, wb, t]

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
		pointInfoList.extend(self.get_撇彎(pointInfoList[-1][1], wl, wr, h))
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
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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
		pointInfoList.extend(self.get_撇鉤(pointInfoList[-1][1], hh, wg, hg))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_橫斜鉤(BaseCurveComputer):
	def checkType(self):
		assert len(self.actionList)>=5, "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[-2])
		endX, endY = self.getPos(self.pointList[-1])
		w = mid1X - startX
		w2 = mid2X - mid1X
		h2 = mid2Y - mid1Y
#		w3 = mid3X - mid2X
#		hh = mid5Y - mid3Y
#		wg = mid3X - endX
		hg = mid2Y - endY
		self.info = [w, w2, h2, hg]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		w = self.getInfo()[0]
		w2 = self.getInfo()[1]
		h2 = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_斜鉤(pointInfoList[-1][1], w2, h2, hg))
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
		self.info = [mid1X - startX, mid2Y - mid1Y, mid3X - mid2X, endY-mid3Y]

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
		self.info = [endY - startY]

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
		self.info = [midY - startY, endX - midX]

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
		self.info = [midY - startY, endX - midX, midY - endY]

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
		self.info = [mid1Y - startY, mid2X - mid1X, endY-mid2Y]

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
		wp = mid1X - startX
		hp = mid1Y - startY
		w = mid2X - mid1X
		h = mid4Y - mid2Y
		wg = mid2X - endX
		hg = mid4Y - endY
		self.info = [hp, w, h, wg, hg]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		hp = self.getInfo()[0]
		w = self.getInfo()[1]
		h = self.getInfo()[2]
		wg = self.getInfo()[3]
		hg = self.getInfo()[4]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎(pointInfoList[-1][1], hp))
		pointInfoList.extend(self.get_橫(pointInfoList[-1][1], w))
		pointInfoList.extend(self.get_撇鉤(pointInfoList[-1][1], h, wg, hg))
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
		self.info = [hl, wl, cr, tl]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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

		cr = min(int((endX - startX)/3), int((endY - startY)/3), 0x20)
		w = endX - startX - cr
		h = endY - startY - cr
		self.info = [w, h, cr]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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
		w=startX-endX
		h1=endY-startY
		h2=midY-endY
		self.info = [h1, h2, w]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		h1 = self.getInfo()[0]
		h2 = self.getInfo()[1]
		w = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_豎鉤(pointInfoList[-1][1], h1, h2, w))
		pointInfoList.extend(self.get_趯(pointInfoList[-1][1], int(w/2), int(w/2)))
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
		w=mid2X-startX
		h=mid2Y-startY
		ht=mid2Y-endY
		self.info = [w, h, ht]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		w = self.getInfo()[0]
		h = self.getInfo()[1]
		ht = self.getInfo()[2]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_斜鉤(pointInfoList[-1][1], w, h, ht))
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
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		w1 = self.getInfo()[0]
		h1 = self.getInfo()[1]
		wg = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_彎鉤(pointInfoList[-1][1], w1, h1))
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
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
		wp = self.getInfo()[0]
		hp = self.getInfo()[1]
		wg = self.getInfo()[2]
		hg = self.getInfo()[3]

		startPoint = self.getStartPoint()
		pointInfoList = [(False, startPoint)]
		pointInfoList.extend(self.get_彎鉤(pointInfoList[-1][1], wp, hp))
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

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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
		w=startX-endX
		h=endY-startY
		self.info = [w, h]

	def genNewExp(self):
		startEnd = self.getStartEnd()
		startPoint = startEnd[:2]
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
		pointInfoList.extend(self.get_點(pointInfoList[-1][1], w2, h2))
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
		w = startX - endX
		h = endY - startY
		self.info = [w, h]

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
		self.info = [endX - startX, startY - endY]

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
		w = mid1X - startX
		wn = endX - mid1X
		hn = endY - mid1Y
		self.info = [w, wn, hn]

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
		pointInfoList.extend(self.get__臥捺(pointInfoList[-1][1], w, h))
		self.newExp = self.genStrokeString(pointInfoList)

class CurveComputer_挑捺(BaseCurveComputer):
	def checkType(self):
		assert self.actionList==['0000', '0001', '0002', '0001', ], "Error: {0}".format(self.getErrorInfo())

	def genInfo(self):
		startX, startY = self.getPos(self.pointList[0])
		mid1X, mid1Y = self.getPos(self.pointList[1])
		mid2X, mid2Y = self.getPos(self.pointList[2])
		endX, endY = self.getPos(self.pointList[-1])
		w = mid1X - startX
		h = startY - mid1Y
		wn = endX - mid1X
		hn = endY - mid1Y
		self.info = [w, h, wn, hn]

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

	def genNewExp(self):
		scope = self.getScope()
		left, top, right, bottom = scope
		CX = left + (right-left)//2
		CY = top + (bottom-top)//2

		a = self.getInfo()[0]
		b = self.getInfo()[1]
		startPoint = [CX, CY - b]
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
		"{0:02X}{1:02X},{2:02X}{3:02X}".format(*computer.getStartEnd()),
		computer.getNewExp(), exp,
		computer.getInfo(),
		)

main()

