from injector import inject
from injector import singleton

import model
from Constant import MethodName, Package
from Constant import MainCharDescManager, ImCharDescManager
from model.OperatorManager import OperatorManager
from model.CodeInfoManager import CodeInfoManager

@singleton
class StructureManager:
	@inject
	def __init__(self, \
			inputMethod: MethodName, \
			operationManager: OperatorManager, \
			codeInfoManager: CodeInfoManager, \
			mainDescMgr: MainCharDescManager, \
			imDescMgr: ImCharDescManager, \
			):
		self.operationManager=operationManager
		self.codeInfoManager=codeInfoManager
		self.mainDescMgr=mainDescMgr
		self.imDescMgr=imDescMgr

		self._loadData(inputMethod)

	def _loadData(self, inputMethod):
		self._loadMainData()
		self._loadImData(inputMethod)

	def _loadMainData(self):
		mainDir = "gen/qhdata/main/"
		mainComponentList = [
			mainDir + 'CJK.yaml',
			mainDir + 'CJK-A.yaml',
			mainDir + 'component/CJK.yaml',
			mainDir + 'component/CJK-A.yaml',
			mainDir + 'style.yaml',
		]
		mainTemplateFile = mainDir + 'template.yaml'

		self.mainDescMgr.loadData(mainComponentList)
		self.mainDescMgr.loadSubstituteRules(mainTemplateFile)

	def _loadImData(self, inputMethod):
		imDir = "gen/qhdata/%s/"%inputMethod
		imComponentList = [
			imDir + 'style.yaml'
		]
		imRadixList = [
			imDir + 'radix/CJK.yaml',
			imDir + 'radix/CJK-A.yaml',
			imDir + 'radix/adjust.yaml'
		]
		imSutstitueFile = imDir + 'substitute.yaml'

		self.imDescMgr.loadData(imComponentList)
		self.imDescMgr.loadSubstituteRules(imSutstitueFile)

		self.codeInfoManager.loadRadix(imRadixList)

		resetRadixNameList=self.codeInfoManager.getResetRadixList()
		self.imDescMgr.resetCompoundCharactersToBeRadix(resetRadixNameList)

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
