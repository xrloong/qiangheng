import abc

from parser.model import CharacterDecompositionModel

from ..helper import StructureParser
from .StructureDescription import DecompositionDescription
from .StructureDescription import StructureDescription

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
	def __init__(self, model: CharacterDecompositionModel):
		self.__name = model.name

		decompositions = tuple(DecompositionDescription(structureModel) for structureModel in model.structureSet)
		self.__decompositions = decompositions

	@property
	def name(self):
		return self.__name

	@property
	def structures(self):
		return self.__structures

	def prepareStructures(self, structureParser: StructureParser):
		self.__structures = tuple(decomposition.generateStructure(structureParser) for decomposition in self.__decompositions)

