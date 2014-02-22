
# 視此模式為獨體模式（Singleton）。
from im.gear import CodeInfoManager

__state_IMPackage=None
codeInfoManager=None

def __init__(self):
	pass

def setIMPackage(imPackage):
	global __state_IMPackage
	global codeInfoManager

	__state_IMPackage=imPackage

	codeInfoEncoder=imPackage.CodeInfoEncoder()
	radixParser=imPackage.RadixParser(imPackage.IMName, codeInfoEncoder)
	codeInfoManager=CodeInfoManager.CodeInfoManager(radixParser, codeInfoEncoder)

def getCodeInfoManager():
	return codeInfoManager

