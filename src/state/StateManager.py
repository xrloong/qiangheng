
# 視此模式為獨體模式（Singleton）。
from im.gear import CodeInfoManager
from im.gear.CharacterDescriptionRearranger import CharacterDescriptionRearranger

__state_IMPackage=None
characterDescriptionRearrangerGenerator=None
codeInfoManager=None

def __init__(self):
	pass

def setIMPackage(imPackage):
	global __state_IMPackage
	global characterDescriptionRearrangerGenerator
	global codeInfoManager

	__state_IMPackage=imPackage

	characterDescriptionRearrangerGenerator=CharacterDescriptionRearranger

	codeInfoEncoder=imPackage.CodeInfoEncoder()
	radixParser=imPackage.RadixParser(imPackage.IMName, codeInfoEncoder)
	codeInfoManager=CodeInfoManager.CodeInfoManager(radixParser, codeInfoEncoder)

def getCodeInfoManager():
	return codeInfoManager

