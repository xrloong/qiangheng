from .SOCodeInfoEncoder import SOCodeInfoEncoder
from ..DynamicComposition.DCRadixManager import DCRadixManager

class SORadixManager(DCRadixManager):
	def __init__(self, nameInputMethod):
		DCRadixManager.__init__(self, "動態組字")

	def createEncoder(self):
		return SOCodeInfoEncoder()

