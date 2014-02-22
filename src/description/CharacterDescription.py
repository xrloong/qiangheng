from description import CharacterProperty

class CharacterDescription:
	def __init__(self, name, structList=[]):
		self.name=name
		self.structList=structList

		self.charProp=CharacterProperty.CharacterProperty()

	def getName(self):
		return self.name

	def getStructureList(self):
		return self.structList

	def setStructureList(self, structList):
		self.structList=structList

	def extendStructureList(self, structList):
		self.structList.extend(structList)

	def getCharacterProperty(self):
		return self.charProp.getProperty()

	def updateCharacterProperty(self, prop):
		self.charProp.updateProperty(prop)

	def getFrequency(self):
		return self.charProp.getFrequency()

