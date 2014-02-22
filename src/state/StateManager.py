
# 視此模式為獨體模式（Singleton）。

STATE_QUANTITY_NONE=0
STATE_QUANTITY_ONE=1
STATE_QUANTITY_MULTIPLE=2

__state_Quantity=STATE_QUANTITY_NONE
__state_IMModule=None
codeInfoGenerator=None

def __init__(self):
	pass

def setQuantity(quantity):
	global __state_Quantity
	__state_Quantity=quantity

def getQuantity():
	return __state_Quantity

def setIMModule(imModule):
	global __state_IMModule
	global codeInfoGenerator

	__state_IMModule=imModule
	codeInfoGenerator=imModule.CodeInfoGenerator

def getIMModule():
	return __state_IMModule

