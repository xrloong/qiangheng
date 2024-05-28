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
	def __init__(self, model: CharacterDecompositionModel, structureParser: StructureParser):
		self.__name = model.name

		decompositions = tuple(DecompositionDescription(structureModel) for structureModel in model.structureSet)
		structures = tuple(decomposition.generateStructure(structureParser) for decomposition in decompositions)
		self.__structures = structures

	@property
	def name(self):
		return self.__name

	@property
	def structures(self):
		return self.__structures

