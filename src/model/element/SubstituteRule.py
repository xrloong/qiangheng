from model.tree.regexp import compile

class SubstituteRule:
	def __init__(self, pattern, replacement):
		self.pattern=pattern
		self.replacement=replacement
		self.tre=compile(pattern)

	def getPattern(self):
		return self.pattern

	def getReplacement(self):
		return self.replacement

	def getTRE(self):
		return self.tre
