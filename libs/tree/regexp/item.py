class TreeRegExp:
	def __init__(self):
		self.children = []
		self.prop={}

		self.flagWithStar = False
		self.flagIsDot = False

		self.matched=[]

	def __str__(self):
		return "%s"%self.prop

	@staticmethod
	def generateDot():
		tre=TreeRegExp()
		tre.setAsDot()
		return tre

	def updateProp(self, prop):
		self.prop.update(prop)

	def setChildren(self, children):
		self.children=children


	def setAsDot(self):
		self.flagIsDot = True

	def setWithStar(self):
		self.flagWithStar = True

	def isWithStar(self):
		return self.flagWithStar

	def isDot(self):
		return self.flagIsDot

	def setMatched(self, matched):
		self.matched = matched

	def getMatched(self):
		return self.matched

	def getAll(self):
		def traversal(c):
			l.append(c)
			for child in c.children:
				traversal(child)
		l=[]
		traversal(self);
		return l;

	def getComp(self, n):
		s, t=self.countComp(0, n)
		if s==n:
			return t
		else:
			return None

	def countComp(self, m, target):
		if m==target:
			return (m, self)
		else:
			s=m
			t=self
			for c in self.children:
				s, t=c.countComp(s+1, target)
				if(s==target):
					return s, t
			return (s, t)

class MatchResult:
	def __init__(self):
		self.result=False
		self.matched={}

	def setTrue(self):
		self.result=True

	def setFalse(self):
		self.result=False

	def isMatched(self):
		return self.result

class TreeProxy:
	def __init__(self):
		pass

	def getChildren(self, tree):
		return []

	def matchSingle(self, tre, tree):
		return True

class BasicTreeProxy:
	def __init__(self):
		pass

	def getChildren(self, tree):
		return tree.get("children", [])

	def matchSingle(self, tre, tree):
		prop=tre.prop

		isMatch = True
		if "名稱" in prop:
			isMatch &= prop.get("名稱") == tree.get("name")

		if "運算" in prop:
			isMatch &= prop.get("運算") == tree.get("operator")

		return isMatch

	def generateLeafNode(self, nodeName):
		return None

	def generateNode(self, operatorName, children):
		return None

	def generateLeafNodeByReference(self, referencedNode, index):
		return None


class TreeNodeGenerator:
	def generateLeafNode(self, nodeName):
		return None

	def generateNode(self, operatorName, children):
		return None

	def generateLeafNodeByReference(self, referencedNode, index):
		return None

