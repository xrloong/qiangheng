
# 視此模式為獨體模式（Singleton）。
from im.gear import CodeInfoManager

__state_IMPackage=None
codeInfoManager=None
structureRearranger=None

def __init__(self):
	pass

def setIMPackage(imPackage):
	global __state_IMPackage
	global codeInfoManager
	global structureRearranger

	__state_IMPackage=imPackage

	codeInfoManager=CodeInfoManager.CodeInfoManager(imPackage)

	structureRearranger=imPackage.StructureRearranger()

def getCodeInfoManager():
	return codeInfoManager

def getStructureRearranger():
	return structureRearranger

