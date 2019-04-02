from injector import inject
from injector import singleton

from model.OperatorManager import OperatorManager

from .CharacterDescriptionManager import CharacterDescriptionManager
from .CharacterDescriptionManager import RadixManager

@singleton
class StructureManager:
	@inject
	def __init__(self, \
			operationManager: OperatorManager, \
			mainDescMgr: CharacterDescriptionManager, \
			radixManager: RadixManager, \
			):
		self.operationManager=operationManager
		self.mainDescMgr=mainDescMgr
		self.radixManager=radixManager

		self._loadData()

	def _loadData(self):
		self._loadMainData()
		self._loadImData()

	def _loadMainData(self):
		self.mainDescMgr.loadData()
		self.mainDescMgr.loadSubstituteRules()

	def _loadImData(self):
		self.radixManager.loadSubstituteRules()
		self.radixManager.loadRadix()

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
		return self.mainDescMgr.getSubstituteRuleList()

	def getSubstituteRuleList(self):
		return self.radixManager.getSubstituteRuleList()

	def generateOperator(self, operatorName):
                operationManager=self.operationManager
                return operationManager.generateOperator(operatorName)
