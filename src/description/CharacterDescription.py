
class CharacterDescription:
	def __init__(self, name, charProp):
		self.name=name
		self.structList=[]

		self.charProp=charProp

	def getName(self):
		return self.name

	def getStructureList(self):
		return self.structList

	def setStructureList(self, structList):
		self.structList=structList

	def extendStructureList(self, structList):
		self.structList.extend(structList)

	def getCharacterProperty(self):
		return self.charProp

	def updateCharacterProperty(self, charProp):
		self.charProp.update(charProp)

