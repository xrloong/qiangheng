from typing import Optional

from parser.model import CharacterDecompositionModel
from parser.model import CharacterDecompositionSetModel

from ..helper import StructureParser
from .StructureDescription import DecompositionDescription
from .StructureDescription import StructureDescription

class CharacterDescription:
	def __init__(self, name: Optional[str] = None, model: Optional[CharacterDecompositionModel] = None):
		if model is not None:
			self.__name = model.name

			decompositions = tuple(DecompositionDescription(structureModel) for structureModel in model.structureSet)
			self.__decompositions = decompositions
			self.__structures = None
		elif name is not None:
			self.__name = name
			self.__decompositions = ()
			self.__structures = ()

	@property
	def name(self):
		return self.__name

	@property
	def structures(self):
		return self.__structures

	def prepareStructures(self, structureParser: StructureParser):
		if self.__structures is not None:
			return

		def generateStructure(decomposition):
			structureDesc = structureParser.convert(decomposition.node, decomposition.font)
			return structureDesc

		self.__structures = tuple(generateStructure(decomposition) for decomposition in self.__decompositions)

class CharacterDecompositionSet:
	def __init__(self, model: CharacterDecompositionSetModel):
		self.__charDescs = tuple(CharacterDescription(model = decompositionModel) for decompositionModel in model.decompositionSet)

	@property
	def charDescs(self):
		return self.__charDescs

	def prepareStructures(self, structureParser: StructureParser):
		for charDesc in self.charDescs:
			charDesc.prepareStructures(structureParser)
