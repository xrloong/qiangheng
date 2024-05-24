from parser.model import SubstituteRuleModel

from model.tree.regexp import compile

class SubstituteRule:
	def __init__(self, model: SubstituteRuleModel):
		self.pattern = model.pattern
		self.replacement = model.replacement
		self.tre = compile(self.pattern)

	def getPattern(self):
		return self.pattern

	def getReplacement(self):
		return self.replacement

	def getTRE(self):
		return self.tre
