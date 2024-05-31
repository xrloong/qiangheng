from injector import inject
from injector import singleton

from .element.CodingConfig import CodingConfig
from .helper import StructureConverter

from .CharacterDescriptionManager import CompositionManager
from .CharacterDescriptionManager import SubstituteManager
from .CharacterDescriptionManager import RadixManager

class QHDataCommonDataManager:
	@inject
	def __init__(self,
			compositionManager: CompositionManager,
			templateManager: SubstituteManager,
			):
		self.__compositionManager = compositionManager
		self.__templateManager = templateManager

	@property
	def compositionManager(self) -> CompositionManager:
		return self.__compositionManager

	@property
	def templateManager(self) -> SubstituteManager:
		return self.__templateManager

	def loadData(self, componentFiles: list[str], templateFiles: list[str]):
		self.compositionManager.loadComponents(componentFiles)
		self.templateManager.loadSubstituteRules(templateFiles)

class QHDataCodingDataManager:
	@inject
	def __init__(self,
			radixManager: RadixManager,
			substituteManager: SubstituteManager,
			):
		self.__radixManager = radixManager
		self.__substituteManager = substituteManager

	@property
	def radixManager(self) -> RadixManager:
		return self.__radixManager

	@property
	def substituteManager(self) -> SubstituteManager:
		return self.__substituteManager

	def loadData(self, radixFiles: list[str], adjustFiles: list[str], substituteFiles: list[str]):
		self.radixManager.loadMainRadicals(radixFiles)
		self.radixManager.loadAdjust(adjustFiles)
		self.substituteManager.loadSubstituteRules(substituteFiles)

	def loadFastCodes(self, fastFile: str):
		fastCodes = self.radixManager.loadFastCodes(fastFile) if fastFile else {}
		return fastCodes

@singleton
class StructureManager:
	@inject
	def __init__(self,
			codingConfig: CodingConfig,

			qhCommonDM: QHDataCommonDataManager,
			qhCodingDM: QHDataCodingDataManager,

			structureConverter: StructureConverter
			):
		self.__codingConfig = codingConfig

		self.__qhCommonDM = qhCommonDM
		self.__qhCodingDM = qhCodingDM

		self.__structureConverter = structureConverter

		self.__loadData()

	@property
	def compositionManager(self) -> CompositionManager:
		return self.__qhCommonDM.compositionManager

	@property
	def templateManager(self) -> SubstituteManager:
		return self.__qhCommonDM.templateManager

	@property
	def substituteManager(self) -> SubstituteManager:
		return self.__qhCodingDM.substituteManager

	@property
	def radixManager(self) -> RadixManager:
		return self.__qhCodingDM.radixManager

	@property
	def commonDM(self) -> QHDataCommonDataManager:
		return self.__qhCommonDM

	@property
	def codingDM(self) -> QHDataCodingDataManager:
		return self.__qhCodingDM

	def __loadData(self):
		codingConfig = self.__codingConfig

		self.commonDM.loadData(
                componentFiles = codingConfig.getCommonComponentFileList(),
                templateFiles = codingConfig.getCommonTemplateFileList(),
                )
		self.codingDM.loadData(
                radixFiles = codingConfig.getSpecificRadixFileList(),
                adjustFiles = codingConfig.getSpecificAdjustFileList(),
                substituteFiles = codingConfig.getSpecificSubstituteFileList(),
                )

	def loadFastCodes(self):
		fastFile = self.__codingConfig.getSpecificFastFile()
		return self.codingDM.loadFastCodes(fastFile = fastFile)

	def queryCharacterDescription(self, character):
		charDesc = self.radixManager.queryRadix(character)
		if not charDesc:
			charDesc = self.compositionManager.queryCharacter(character)
		charDesc.prepareStructures(self.__structureConverter)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

