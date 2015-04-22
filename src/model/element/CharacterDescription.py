
class CharacterDescription:
	def __init__(self, name):
		self.name=name
		self.structList=[]

	def getName(self):
		return self.name

	def getStructureList(self):
		return self.structList

	def setStructureList(self, structList):
		self.structList=structList

	def extendStructureList(self, structList):
		self.structList.extend(structList)

