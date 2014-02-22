from .SOCodeInfoEncoder import SOCodeInfoEncoder
from ..DynamicComposition.DCRadixManager import DCRadixParser

class SORadixParser(DCRadixParser):
	def __init__(self, nameInputMethod, codeInfoEncoder):
		DCRadixParser.__init__(self, "動態組字", codeInfoEncoder)

