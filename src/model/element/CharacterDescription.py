import abc

class AbcCharacterDescription(object, metaclass=abc.ABCMeta):
	@abc.abstractproperty
	def name(self): pass

	@abc.abstractproperty
	def structures(self): pass

class RadicalCharacterDescription(AbcCharacterDescription):
	def __init__(self, name):
		self.__name = name

	@property
	def name(self):
		return self.__name

	@property
	def structures(self):
		return ()

class CharacterDescription(AbcCharacterDescription):
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

