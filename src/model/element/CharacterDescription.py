from typing import Optional

from parser.model import CharacterDecompositionModel
from parser.model import CharacterDecompositionSetModel

from ..helper import StructureConverter
from .StructureDescription import DecompositionDescription

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

	def prepareStructures(self, structureConverter: StructureConverter):
		if self.__structures is not None:
			return

		self.__structures = tuple(structureConverter.convert(decomposition.node, decomposition.font) for decomposition in self.__decompositions)

class CharacterDecompositionSet:
	def __init__(self, model: CharacterDecompositionSetModel):
		self.__charDescs = tuple(CharacterDescription(model = decompositionModel) for decompositionModel in model.decompositionSet)

	@property
	def charDescs(self):
		return self.__charDescs
