
# 視此模式為獨體模式（Singleton）。
from gear import RadixManager
from gear import CodeInfoManager

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
	codeInfoEncoder=imModule.codeInfoEncoder
	characterDescriptionRearrangerGenerator=imModule.CharacterDescriptionRearrangerGenerator

	radixManager=imModule.radixManager
	codeInfoManager=CodeInfoManager.CodeInfoManager(radixManager, codeInfoEncoder)

def getIMModule():
	return __state_IMModule

def getCodeInfoManager():
	return codeInfoManager

