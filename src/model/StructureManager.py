from .CharacterDescriptionManager import CharacterDescriptionManager
from model import StateManager
from model.im.IMMgr import IMMgr

class StructureManager:
	def __init__(self, inputMethod):
		imPackage=IMMgr.getIMPackage(inputMethod)
		StateManager.setIMPackage(imPackage)
		self.imInfo=imPackage.IMInfo()

		self.mainDescMgr=CharacterDescriptionManager()
		self.imDescMgr=CharacterDescriptionManager()
		self.operationManager=StateManager.getOperationManager()
		self.codeInfoManager=StateManager.getCodeInfoManager()

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
			imDir + 'radix/CJK-A.yaml'
		]
		imSutstitueFile = imDir + 'substitute.yaml'

		self.imDescMgr.loadData(imComponentList)
		self.imDescMgr.loadSubstituteRules(imSutstitueFile)

		self.codeInfoManager.loadRadix(imRadixList)

		resetRadixNameList=self.codeInfoManager.getResetRadixList()
		self.imDescMgr.resetCompoundCharactersToBeRadix(resetRadixNameList)

	def getImInfo(self):
		return self.imInfo

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
                operationManager=StateManager.getOperationManager()
                return operationManager.generateOperator(operatorName)

	def getCodeInfoManager(self):
		return StateManager.getCodeInfoManager()
