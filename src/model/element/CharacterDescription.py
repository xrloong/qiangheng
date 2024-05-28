
class CharacterDescription:
	def __init__(self, name):
		self.__name = name
		self.__structures = ()

	@property
	def name(self):
		return self.__name

	@property
	def structures(self):
		return self.__structures

	def setStructureList(self, structures):
		self.__structures = structures

	def extendStructureList(self, structures):
		self.__structures.extend(structures)

