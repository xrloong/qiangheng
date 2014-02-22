
class CodeMappingInfo:
	def __init__(self, name, code, freq, variance):
		self.name=name
		self.code=code
		self.freq=freq
		self.variance=variance

	def getKey(self):
		return [self.getCode(), self.getName(), self.getFrequency(), self.getVariance()]

	def getName(self):
		return self.name

	def getCode(self):
		return self.code

	def getFrequency(self):
		return self.freq

	def getVariance(self):
		return self.variance

