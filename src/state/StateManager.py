
# 視此模式為獨體模式（Singleton）。
from im.gear import CodeInfoManager
from im.gear.CharacterDescriptionRearranger import CharacterDescriptionRearranger

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

	characterDescriptionRearrangerGenerator=CharacterDescriptionRearranger

	radixParser=imModule.radixParser
	codeInfoManager=CodeInfoManager.CodeInfoManager(radixParser.getEncoder())

def getIMModule():
	return __state_IMModule

def getCodeInfoManager():
	return codeInfoManager

