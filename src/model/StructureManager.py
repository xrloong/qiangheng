from injector import inject
from injector import singleton

from model.OperatorManager import OperatorManager

from .CharacterDescriptionManager import CharacterDescriptionManager
from .CharacterDescriptionManager import ImCharacterDescriptionManager

@singleton
class StructureManager:
	@inject
	def __init__(self, \
			operationManager: OperatorManager, \
			mainDescMgr: CharacterDescriptionManager, \
			imDescMgr: ImCharacterDescriptionManager, \
			):
		self.operationManager=operationManager
		self.mainDescMgr=mainDescMgr
		self.imDescMgr=imDescMgr

		self._loadData()

	def _loadData(self):
		self._loadMainData()
		self._loadImData()

	def _loadMainData(self):
		self.mainDescMgr.loadData()
		self.mainDescMgr.loadSubstituteRules()

	def _loadImData(self):
		self.imDescMgr.loadSubstituteRules()
		self.imDescMgr.loadRadix()

	def getAllCharacters(self):
		return set(self.mainDescMgr.getAllCharacters()) | set(self.imDescMgr.getAllCharacters()) 

	def queryCharacterDescription(self, character):
		charDesc = self.imDescMgr.queryCharacterDescription(character)
		if not charDesc:
			charDesc = self.mainDescMgr.queryCharacterDescription(character)
		return charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

	def getTemplateRuleList(self):
		return self.mainDescMgr.getSubstituteRuleList()

	def getSubstituteRuleList(self):
		return self.imDescMgr.getSubstituteRuleList()

	def generateOperator(self, operatorName):
                operationManager=self.operationManager
                return operationManager.generateOperator(operatorName)
