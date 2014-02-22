
# 視此模式為獨體模式（Singleton）。
from im.gear import CodeInfoManager

__state_IMModule=None
characterDescriptionRearrangerGenerator=None
codeInfoManager=None

def __init__(self):
	pass

def setIMModule(imModule):
	global __state_IMModule
	global characterDescriptionRearrangerGenerator
	global codeInfoManager

	__state_IMModule=imModule

	radixManager=imModule.radixManager

	characterDescriptionRearrangerGenerator=radixManager.getCharacterDescriptionRearrangerGenerator()
	codeInfoManager=CodeInfoManager.CodeInfoManager(radixManager)

def getIMModule():
	return __state_IMModule

def getCodeInfoManager():
	return codeInfoManager

