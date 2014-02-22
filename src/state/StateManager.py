
# 視此模式為獨體模式（Singleton）。
from gear import RadixManager

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
	global radixManager

	__state_IMModule=imModule
	codeInfoEncoder=imModule.codeInfoEncoder
	characterDescriptionRearrangerGenerator=imModule.CharacterDescriptionRearrangerGenerator

	radixManager=imModule.radixManager

def getIMModule():
	return __state_IMModule


