from .SPCodeInfo import SPCodeInfo
from .SPCodeInfoEncoder import SPCodeInfoEncoder
from ..base.RadixManager import RadixManager

class SPRadixManager(RadixManager):
	def __init__(self, nameInputMethod):
		RadixManager.__init__(self, nameInputMethod)

	def createEncoder(self):
		return SPCodeInfoEncoder()

