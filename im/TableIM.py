from .NoneIM import NoneIM

class TableIM(NoneIM):
	"輸入法"

	def __init__(self, inputMethod):
		self.inputMethod=inputMethod

	def getName(self, localization):
		return self.inputMethod.getName(localization)

	def getIconFileName(self):
		return self.inputMethod.getIconFileName()

	def getMaxKeyLength(self):
		return self.inputMethod.getMaxKeyLength()

	def getKeyMaps(self):
		return self.inputMethod.getKeyMaps()

	def getKeyList(self):
		return self.inputMethod.getKeyList()

	def setTable(self, tb):
		self.tb=tb

	def genIMMapping(self):
		return self.tb

if __name__=='__main__':
	pass

