
# 視此模式為獨體模式（Singleton）。

__state_IMModule=None
codeInfoGenerator=None

def __init__(self):
	pass

def setIMModule(imModule):
	global __state_IMModule
	global codeInfoGenerator

	__state_IMModule=imModule
	codeInfoGenerator=imModule.CodeInfoGenerator

def getIMModule():
	return __state_IMModule

