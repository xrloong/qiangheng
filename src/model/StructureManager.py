from injector import inject
from injector import singleton

from model.element.CodingConfig import CodingConfig

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
			substituteManager: SubstituteManager
			):
		self.codingConfig = codingConfig
		self.compositionManager = compositionManager
		self.radixManager = radixManager
		self.templateManager = templateManager
		self.substituteManager = substituteManager

		self._loadData()

	def _loadData(self):
		# 從設定中取得相關的檔案列表
		# 共通資料及範本
		componentFiles = self.codingConfig.getCommonComponentFileList()
		templateFiles = self.codingConfig.getCommonTemplateFileList()

		# 主要字根
		radixFiles = self.codingConfig.getSpecificRadixFileList()

		# 個別方法的替代及調整
		substituteFiles = self.codingConfig.getSpecificSubstituteFileList()
		adjustFiles = self.codingConfig.getSpecificAdjustFileList()


		# 載入資料
		# 共通資料及範本
		self.compositionManager.loadComponents(componentFiles)
		self.templateManager.loadSubstituteRules(templateFiles)

		# 主要字根
		self.radixManager.loadRadix(radixFiles)

		# 個別方法的替代及調整
		self.radixManager.loadAdjust(adjustFiles)
		self.substituteManager.loadSubstituteRules(substituteFiles)

	def loadFastCodes(self):
		fastFile = self.codingConfig.getSpecificFastFile()
		fastCodes = self.radixManager.loadFastCodes(fastFile) if fastFile else {}
		return fastCodes

	def getCompositionManager(self):
		return self.compositionManager

	def getRadixManager(self):
		return self.radixManager

	def queryCharacterDescription(self, character):
		charDesc = self.radixManager.queryRadix(character)
		if not charDesc:
			charDesc = self.compositionManager.queryCharacter(character)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

	def getTemplateManager(self):
		return self.templateManager

	def getSubstituteManager(self):
		return self.substituteManager

