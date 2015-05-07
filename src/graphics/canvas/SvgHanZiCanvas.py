from . import HanZiCanvas

class SvgHanZiCanvas(HanZiCanvas.HanZiCanvas):
	def __init__(self, width, height):
		super().__init__(width, height)
		self.expression=""

	def clear(self):
		self.expression=""
		pass

	def moveTo(self, p):
		self.expression +="M %s %s"%(p[0], p[1])
		pass

	def lineTo(self, p, drawoption=None):
		self.expression +="L %s %s"%(p[0], p[1])
		pass

	def qCurveTo(self, cp, p):
		self.expression +="Q %s %s %s %s"%(cp[0], cp[1], p[0], p[1])

	def getExpression(self):
		return self.expression
