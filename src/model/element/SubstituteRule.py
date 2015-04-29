from ..util import TreeRegExp

class SubstituteRule:
	def __init__(self, pattern, replacement):
		self.pattern=pattern
		self.replacement=replacement
		self.tre=TreeRegExp.compile(pattern)

	def getPattern(self):
		return self.pattern

	def getReplacement(self):
		return self.replacement

	def getTRE(self):
		return self.tre
