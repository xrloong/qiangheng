
class CharacterDescription:
	def __init__(self, name, structList=[]):
		self.name=name
		self.structList=structList

		self.prop={}
		self.freq=0
		self.note=""

	def getName(self):
		return self.name

	def getStructureList(self):
		return self.structList

	def setStructureList(self, structList):
		self.structList=structList

	def setProperty(self, prop):
		self.prop.update(prop)

	def updateProperty(self, prop):
		self.prop.update(prop)
		self.freq=self.prop.get('頻率', 0)
		self.note=self.prop.get('註記', "")

	def getFrequency(self):
		return self.freq
