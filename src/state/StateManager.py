
# 視此模式為獨體模式（Singleton）。

__state_IMModule=None
codeInfoEncoder=None
characterDescriptionRearrangerGenerator=None
radixManager=None

def __init__(self):
	pass

def setIMModule(imModule):
	global __state_IMModule
	global codeInfoEncoder
	global characterDescriptionRearrangerGenerator

	__state_IMModule=imModule
	codeInfoEncoder=imModule.codeInfoEncoder
	characterDescriptionRearrangerGenerator=imModule.CharacterDescriptionRearrangerGenerator
	radixManager=imModule.CharacterDescriptionRearrangerGenerator

def getIMModule():
	return __state_IMModule


def setRadixManager(radixMgr):
	global radixManager
	radixManager=radixMgr

