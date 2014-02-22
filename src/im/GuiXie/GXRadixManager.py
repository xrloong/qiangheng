from .GXCodeInfo import GXCodeInfo
from .GXCodeInfoEncoder import GXCodeInfoEncoder
from ..base.RadixManager import RadixParser

class GXRadixParser(RadixParser):
	def createEncoder(self):
		return GXCodeInfoEncoder()

