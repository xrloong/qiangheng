from typing import Optional
from injector import inject

from coding.Base import CodeInfo

from model.helper import StructureConverter

from model.manager import CompositionManager
from model.manager import SubstituteManager
from model.manager import RadixManager

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

	def queryCharacterDescription(self, character):
		charDesc = self.radixManager.queryRadix(character)
		if not charDesc:
			charDesc = self.compositionManager.queryCharacter(character)
		charDesc.prepareStructures(self.__structureConverter)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.compList

	def queryFastCodeInfo(self, character: str) -> Optional[CodeInfo]:
		return self.radixManager.queryFastCodeInfo(character)

