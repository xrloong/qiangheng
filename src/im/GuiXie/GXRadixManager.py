from .GXCodeInfo import GXCodeInfo
from .GXCodeInfoEncoder import GXCodeInfoEncoder
from ..base.RadixManager import RadixManager

class GXRadixManager(RadixManager):
	def __init__(self):
		RadixManager.__init__(self)

	def createEncoder(self):
		return GXCodeInfoEncoder()

