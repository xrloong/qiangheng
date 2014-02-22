from .SPCodeInfo import SPCodeInfo
from .SPCodeInfoEncoder import SPCodeInfoEncoder
from ..base.RadixManager import RadixParser

class SPRadixParser(RadixParser):
	def createEncoder(self):
		return SPCodeInfoEncoder()

