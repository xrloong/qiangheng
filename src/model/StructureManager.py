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
		self.codingConfig=codingConfig
		self.compositionManager=compositionManager
		self.radixManager=radixManager
		self.templateManager=templateManager
		self.substituteManager=substituteManager

		self._loadData()

	def _loadData(self):
		componentFiles = self.codingConfig.getCommonComponentFileList() + self.codingConfig.getSpecificComponentFileList()
		templateFiles = self.codingConfig.getCommonTemplateFileList()
		substituteFiles = self.codingConfig.getSpecificSubstituteFileList()
		radixFiles = self.codingConfig.getSpecificRadixFileList()

		self.compositionManager.loadComponents(componentFiles)
		self.radixManager.loadRadix(radixFiles)
		self.templateManager.loadSubstituteRules(templateFiles)
		self.substituteManager.loadSubstituteRules(substituteFiles)

	def getAllCharacters(self):
		return set(self.compositionManager.getAllCharacters()) | set(self.radixManager.getAllRadixes()) 

	def queryCharacterDescription(self, character):
		charDesc = self.radixManager.queryRadix(character)
		if not charDesc:
			charDesc = self.compositionManager.queryCharacterDescription(character)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

	def getTemplateRuleList(self):
		return self.templateManager.getSubstituteRuleList()

	def getSubstituteRuleList(self):
		return self.substituteManager.getSubstituteRuleList()

