from .SPCodeInfo import SPCodeInfo
from .SPCodeInfoEncoder import SPCodeInfoEncoder
from ..base.RadixManager import RadixManager

class SPRadixManager(RadixManager):
	def __init__(self):
		RadixManager.__init__(self)

	def createEncoder(self):
		return SPCodeInfoEncoder()

