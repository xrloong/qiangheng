from injector import inject
from injector import singleton

from .element.CodingConfig import CodingConfig
from .helper import StructureConverter

from .CharacterDescriptionManager import CompositionManager
from .CharacterDescriptionManager import SubstituteManager
from .CharacterDescriptionManager import RadixManager

@singleton
class StructureManager:
	@inject
	def __init__(self,
			codingConfig: CodingConfig,
			compositionManager: CompositionManager,
			radixManager: RadixManager,
			templateManager: SubstituteManager,
			substituteManager: SubstituteManager,

			structureConverter: StructureConverter
			):
		self.__codingConfig = codingConfig
		self.__compositionManager = compositionManager
		self.__radixManager = radixManager
		self.__templateManager = templateManager
		self.__substituteManager = substituteManager

		self.__structureConverter = structureConverter

		self.__loadData()

	@property
	def compositionManager(self):
		return self.__compositionManager

	@property
	def templateManager(self):
		return self.__templateManager

	@property
	def substituteManager(self):
		return self.__substituteManager

	@property
	def radixManager(self):
		return self.__radixManager

	def __loadData(self):
		# 從設定中取得相關的檔案列表
		# 共通資料及範本
		codingConfig = self.__codingConfig

		componentFiles = codingConfig.getCommonComponentFileList()
		templateFiles = codingConfig.getCommonTemplateFileList()

		# 主要字根
		radixFiles = codingConfig.getSpecificRadixFileList()

		# 個別方法的替代及調整
		substituteFiles = codingConfig.getSpecificSubstituteFileList()
		adjustFiles = codingConfig.getSpecificAdjustFileList()


		# 載入資料
		# 共通資料及範本
		self.compositionManager.loadComponents(componentFiles)
		self.templateManager.loadSubstituteRules(templateFiles)

		# 主要字根
		self.radixManager.loadMainRadicals(radixFiles)

		# 個別方法的替代及調整
		self.radixManager.loadAdjust(adjustFiles)
		self.substituteManager.loadSubstituteRules(substituteFiles)

	def loadFastCodes(self):
		fastFile = self.__codingConfig.getSpecificFastFile()
		fastCodes = self.radixManager.loadFastCodes(fastFile) if fastFile else {}
		return fastCodes

	def queryCharacterDescription(self, character):
		charDesc = self.radixManager.queryRadix(character)
		if not charDesc:
			charDesc = self.compositionManager.queryCharacter(character)
		charDesc.prepareStructures(self.__structureConverter)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

