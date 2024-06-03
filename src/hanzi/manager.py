from injector import inject

from model.helper import StructureConverter

from model.CharacterDescriptionManager import CompositionManager
from model.CharacterDescriptionManager import SubstituteManager
from model.CharacterDescriptionManager import RadixManager

from model.datamanager import QHDataManager

class StructureManager:
	@inject
	def __init__(self,
			qhDM: QHDataManager,
			structureConverter: StructureConverter
			):
		self.__qhDM = qhDM
		self.__structureConverter = structureConverter

	@property
	def compositionManager(self) -> CompositionManager:
		return self.__qhDM.compositionManager

	@property
	def templateManager(self) -> SubstituteManager:
		return self.__qhDM.templateManager

	@property
	def substituteManager(self) -> SubstituteManager:
		return self.__qhDM.substituteManager

	@property
	def radixManager(self) -> RadixManager:
		return self.__qhDM.radixManager

	def loadFastCodes(self):
		return self.__qhDM.loadFastCodes()

	def queryCharacterDescription(self, character):
		charDesc = self.radixManager.queryRadix(character)
		if not charDesc:
			charDesc = self.compositionManager.queryCharacter(character)
		charDesc.prepareStructures(self.__structureConverter)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

