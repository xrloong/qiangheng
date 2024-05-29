import abc

from parser.model import CharacterDecompositionModel
from parser.model import CharacterDecompositionSetModel

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
		def generateStructure(decomposition):
			structureDesc = structureParser.parse(decomposition.expression)
			structureDesc.updateFontVariance(decomposition.font)
			return structureDesc

		self.__structures = tuple(generateStructure(decomposition) for decomposition in self.__decompositions)

class CharacterDecompositionSet:
	def __init__(self, model: CharacterDecompositionSetModel):
		self.__charDescs = tuple(CharacterDescription(decompositionModel) for decompositionModel in model.decompositionSet)

	@property
	def charDescs(self):
		return self.__charDescs

	def prepareStructures(self, structureParser: StructureParser):
		for charDesc in self.charDescs:
			charDesc.prepareStructures(structureParser)
