from .GXCodeInfo import GXCodeInfo
from .GXCodeInfoEncoder import GXCodeInfoEncoder
from ..base.RadixManager import RadixManager

class GXRadixManager(RadixManager):
	def __init__(self, nameInputMethod):
		RadixManager.__init__(self, nameInputMethod)

	def createEncoder(self):
		return GXCodeInfoEncoder()

