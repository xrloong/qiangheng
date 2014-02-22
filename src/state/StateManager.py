
# 視此模式為獨體模式（Singleton）。
from im.gear.CodeInfoManager import CodeInfoManager
from im.gear.OperatorManager import OperatorManager

__state_IMPackage=None
codeInfoManager=None
operationManager=None

def __init__(self):
	pass

def setIMPackage(imPackage):
	global __state_IMPackage
	global codeInfoManager
	global operationManager

	__state_IMPackage=imPackage

	codeInfoManager=CodeInfoManager(imPackage)

	operationManager=OperatorManager(imPackage)

def getCodeInfoManager():
	return codeInfoManager

def getOperationManager():
	return operationManager

