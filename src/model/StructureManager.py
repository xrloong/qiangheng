from injector import inject
from injector import singleton

from .CharacterDescriptionManager import CharacterDescriptionManager
from .CharacterDescriptionManager import SubstituteManager
from .CharacterDescriptionManager import RadixManager

@singleton
class StructureManager:
	@inject
	def __init__(self,
			mainDescMgr: CharacterDescriptionManager,
			radixManager: RadixManager,
			templateManager: SubstituteManager,
			substituteManager: SubstituteManager
			):
		self.mainDescMgr=mainDescMgr
		self.radixManager=radixManager
		self.templateManager=templateManager
		self.substituteManager=substituteManager

		self._loadData()

	def _loadData(self):
		self.mainDescMgr.loadData()
		self.radixManager.loadRadix()
		self.templateManager.loadTemplates()
		self.substituteManager.loadSubstitutes()

	def getAllCharacters(self):
		return set(self.mainDescMgr.getAllCharacters()) | set(self.radixManager.getAllCharacters()) 

	def queryCharacterDescription(self, character):
		charDesc = self.radixManager.queryCharacterDescription(character)
		if not charDesc:
			charDesc = self.mainDescMgr.queryCharacterDescription(character)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

	def getTemplateRuleList(self):
		return self.templateManager.getSubstituteRuleList()

	def getSubstituteRuleList(self):
		return self.substituteManager.getSubstituteRuleList()

