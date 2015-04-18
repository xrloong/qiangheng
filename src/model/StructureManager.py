from description.CharacterDescriptionManager import CharacterDescriptionManager
from state import StateManager
from im.IMMgr import IMMgr

class StructureManager:
	def __init__(self, inputMethod):
		imPackage=IMMgr.getIMPackage(inputMethod)
		StateManager.setIMPackage(imPackage)
		self.imInfo=imPackage.IMInfo()

		mainComponentList = [
			'gen/qhdata/main/CJK.yaml',
			'gen/qhdata/main/CJK-A.yaml',
			'gen/qhdata/main/component/CJK.yaml',
			'gen/qhdata/main/component/CJK-A.yaml',
			'gen/qhdata/main/style.yaml',
		]
		imComponentList = [
			'gen/qhdata/%s/style.yaml'%inputMethod,
		]
		imRadixList = [
			'gen/qhdata/%s/radix/CJK.yaml'%inputMethod,
			'gen/qhdata/%s/radix/CJK-A.yaml'%inputMethod,
		]
		mainTemplateFile = 'gen/qhdata/main/template.yaml'
		imSutstitueFile = 'gen/qhdata/%s/substitute.yaml'%inputMethod

		StateManager.getOperationManager().loadTemplates(mainTemplateFile)
		StateManager.getOperationManager().loadSubstituteRules(imSutstitueFile)
		StateManager.getCodeInfoManager().loadRadix(imRadixList)

		self.descMgr=CharacterDescriptionManager()

		self.loadData(mainComponentList, imComponentList)

	def getImInfo(self):
		return self.imInfo

	def loadData(self, mainComponentList, imComponentList):
		self.descMgr.loadData(mainComponentList + imComponentList)

	def getAllCharacters(self):
		return self.descMgr.getAllCharacters()

	def getDescriptionManager(self):
		return self.descMgr

	def queryCharacterDescription(self, character):
		return self.descMgr.queryCharacterDescription(character)

	def queryChildren(self, charDesc):
		return self.descMgr.queryChildren(charDesc)

	def getTemplatePatternList(self):
                operationManager=StateManager.getOperationManager()
                return operationManager.getTemplatePatternList()

	def getSubstitutePatternList(self):
                operationManager=StateManager.getOperationManager()
                return operationManager.getSubstitutePatternList()

	def rearrangeStructureSingleLevel(self, structDesc):
                operationManager=StateManager.getOperationManager()
                return operationManager.rearrangeStructureSingleLevel(structDesc)

	def generateOperator(self, operatorName):
                operationManager=StateManager.getOperationManager()
                return operationManager.generateOperator(operatorName)

	def getCodeInfoManager(self):
		return StateManager.getCodeInfoManager()
